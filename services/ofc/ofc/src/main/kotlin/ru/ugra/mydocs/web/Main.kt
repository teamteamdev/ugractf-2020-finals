package ru.ugra.mydocs.web

import freemarker.cache.ClassTemplateLoader
import io.ktor.application.*
import io.ktor.features.StatusPages
import io.ktor.features.statusFile
import io.ktor.freemarker.FreeMarker
import io.ktor.freemarker.FreeMarkerContent
import io.ktor.http.*
import io.ktor.http.content.resources
import io.ktor.http.content.static
import io.ktor.request.receiveParameters
import io.ktor.response.respond
import io.ktor.response.respondRedirect
import io.ktor.routing.get
import io.ktor.routing.post
import io.ktor.routing.routing
import io.ktor.server.engine.embeddedServer
import io.ktor.server.jetty.Jetty
import io.ktor.sessions.Sessions
import io.ktor.sessions.SessionStorageMemory
import io.ktor.sessions.cookie
import io.ktor.sessions.get
import io.ktor.sessions.sessions
import io.ktor.sessions.set
import io.ktor.utils.io.charsets.*
import ru.ugra.mydocs.certs.Certificate
import ru.ugra.mydocs.certs.PkiStorage
import ru.ugra.mydocs.certs.Signer
import ru.ugra.mydocs.db.Database
import ru.ugra.mydocs.db.User
import ru.ugra.mydocs.security.Challenger
import ru.ugra.mydocs.utils.isEnum
import ru.ugra.mydocs.utils.validate
import java.math.BigInteger
import java.nio.charset.StandardCharsets.UTF_8

fun main() {
    val mongoDb = Database()
    val pkiStorage = PkiStorage()
    val signer = Signer()

    embeddedServer(Jetty, 8080) {
        install(FreeMarker) {
            templateLoader = ClassTemplateLoader(this::class.java.classLoader, "templates")
        }

        install(Sessions) {
            cookie<UserSession>("ga", SessionStorageMemory()) {
                cookie.path = "/"
            }
        }

        install(StatusPages) {
            statusFile(HttpStatusCode.BadRequest, HttpStatusCode.Forbidden, filePattern="noservice.html")
        }

        routing {
            static("/static") {
                resources("static")
            }

            get("/recent") {
                val profile = call.sessions.get<UserSession>()?.enum
                    ?.let { enum -> mongoDb.getOne(enum) }
                call.respond(
                    FreeMarkerContent(
                        "users.ftl",
                        mapOf(
                            "users" to mongoDb.getLatest().map {
                                it to pkiStorage.get(it.enum)
                            },
                            "profile" to profile
                        )
                    )
                )
            }

            get("/securePkiPage") {
                val enum = call.sessions.get<UserSession>()?.enum
                    ?: return@get call.respondRedirect("/secureApplyPage")

                val profile = mongoDb.getOne(enum)

                call.respond(FreeMarkerContent("pki.ftl", mapOf(
                    "profile" to profile
                )))
            }

            post("/securePkiPage") {
                val enum = call.sessions.get<UserSession>()?.enum
                    ?: return@post call.respondRedirect("/secureApplyPage")

                val profile = mongoDb.getOne(enum)

                val postParameters = call.receiveParameters()
                val password = postParameters["password"] ?: return@post call.respond(HttpStatusCode.BadRequest)

                val extCert = Challenger.newCert(password)
                val certificate = signer.sign(Certificate(
                    extCert.base,
                    extCert.modulo,
                    extCert.result,
                    enum
                ))

                pkiStorage.put(enum, extCert)
                pkiStorage.put(enum, certificate)

                call.respond(FreeMarkerContent("certs.ftl", mapOf(
                    "extCert" to extCert,
                    "certificate" to certificate,
                    "profile" to profile
                ), contentType = ContentType.Text.Plain.withCharset(UTF_8)))
            }

            get("/secureLoginChallenge") {
                val challenge = Challenger.challenge()
                call.sessions.set(UserSession(challenge=challenge))
                call.respond(FreeMarkerContent("login.ftl", mapOf(
                    "challenge" to challenge
                )))
            }

            post("/secureLoginChallenge") {
                val challenge = call.sessions.get<UserSession>()?.challenge
                    ?: return@post call.respond(FreeMarkerContent("nologin.ftl", null))

                val postParameters = call.receiveParameters()
                val key = postParameters["key"] ?: return@post call.respond(FreeMarkerContent("nologin.ftl", null))
                val high = postParameters["high"] ?: return@post call.respond(FreeMarkerContent("nologin.ftl", null))
                val low = postParameters["low"] ?: return@post call.respond(FreeMarkerContent("nologin.ftl", null))

                val certificate = Certificate.unserialize(key)
                val highBi = BigInteger(high)
                val lowBi = BigInteger(low)

                var good = Challenger.checkChallenge(certificate, challenge, highBi, lowBi)

                if (!good) return@post call.respond(FreeMarkerContent("nologin.ftl", null))

                val num = certificate.enum
                call.sessions.set(UserSession(enum=num))
                call.respondRedirect("/")
            }

            get("/secureApplyPage") {
                call.respond(FreeMarkerContent("apply.ftl", null))
            }

            get("/service") {
                call.respond(HttpStatusCode.Forbidden)
            }

            post("/secureApplyPage") {
                val postParameters = call.receiveParameters()
                val enum = postParameters["enum"] ?: return@post call.respond(HttpStatusCode.BadRequest)
                validate(isEnum(enum)) ?: return@post call.respond(HttpStatusCode.BadRequest)
                if (mongoDb.hasEnum(enum)) return@post call.respondRedirect("/secureLoginChallenge")

                val codeword = postParameters["codeword"] ?: ""

                val num = enum.toLong()
                val user = User(num, codeword)
                mongoDb.save(user)

                call.sessions.set(UserSession(enum=num))
                call.respondRedirect("/")
            }

            get("/") {
                val enum = call.sessions.get<UserSession>()?.enum
                    ?: return@get call.respondRedirect("/secureApplyPage")

                call.respond(FreeMarkerContent(
                    "main.ftl",
                    mapOf(
                        "profile" to mongoDb.getOne(enum),
                        "actualCertificate" to pkiStorage.get(enum)
                    )
                ))
            }
        }
    }.start(wait = true)
}

