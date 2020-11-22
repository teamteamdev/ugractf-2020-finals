package ru.ugra.mydocs.certs

import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.math.BigInteger

data class ExtendedCertificate(
    val base: BigInteger,
    val modulo: BigInteger,
    val result: BigInteger,
    val exponent: BigInteger,
    val codeword: String
): Certificated {
    @Serializable
    private data class StringCertificate(
        val base: String,
        val modulo: String,
        val result: String,
        val exponent: String,
        val codeword: String
    )

    override fun serialize(): String {
        return Json.encodeToString(StringCertificate(
            base.toString(),
            modulo.toString(),
            result.toString(),
            exponent.toString(),
            codeword
        ))
    }
}
