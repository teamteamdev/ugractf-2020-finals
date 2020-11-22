package ru.ugra.mydocs.certs

import kotlinx.serialization.Serializable
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.math.BigInteger

data class Certificate(
    val base: BigInteger,
    val modulo: BigInteger,
    val result: BigInteger,
    val enum: Long,
    val signatureHigh: BigInteger = BigInteger.ZERO,
    val signatureLow: BigInteger = BigInteger.ZERO
): Certificated {
    @Serializable
    private data class StringCertificate(
        val base: String,
        val modulo: String,
        val result: String,
        val enum: String,
        val signatureHigh: String,
        val signatureLow: String
    )

    override fun serialize(): String {
        return Json.encodeToString(StringCertificate(
            base.toString(),
            modulo.toString(),
            result.toString(),
            enum.toString(),
            signatureHigh.toString(),
            signatureLow.toString()
        ))
    }

    companion object {
        fun unserialize(input: String): Certificate {
            val sc = Json.decodeFromString<StringCertificate>(input)

            return Certificate(
                BigInteger(sc.base),
                BigInteger(sc.modulo),
                BigInteger(sc.result),
                sc.enum.toLong(),
                BigInteger(sc.signatureHigh),
                BigInteger(sc.signatureLow)
            )
        }
    }
}
