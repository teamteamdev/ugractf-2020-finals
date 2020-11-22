package ru.ugra.mydocs.certs

import ru.ugra.mydocs.utils.positiveMod
import java.io.File
import java.math.BigInteger
import java.security.SecureRandom

class Signer {
    private val modulo: BigInteger
    private val lowModulo: BigInteger
    private val base: BigInteger
    private val exponent: BigInteger
    private val result: BigInteger
    private val rnd: SecureRandom = SecureRandom()

    init {
        val lines = mutableListOf<String>()
        File("/keys").useLines { lines.addAll(it) }
        modulo = BigInteger(lines[0])
        base = BigInteger(lines[1])
        exponent = BigInteger(lines[2])
        result = BigInteger(lines[3])

        lowModulo = modulo - BigInteger.ONE
    }

    private fun hash(certificate: Certificate): BigInteger {
        var hash = certificate.result
        hash *= POWER
        hash += certificate.modulo
        hash *= POWER
        hash += certificate.base
        hash *= POWER
        hash += BigInteger.valueOf(certificate.enum)
        hash %= modulo

        return hash
    }

    fun sign(certificate: Certificate): Certificate {
        val h = hash(certificate)
        val midExponent = BigInteger.probablePrime(256, rnd)

        val high = base.modPow(midExponent, modulo)

        val lowLeft = h - exponent * high
        val inverse = midExponent.modInverse(lowModulo)

        return certificate.copy(
            signatureHigh = high,
            signatureLow = positiveMod(lowLeft * inverse, lowModulo)
        )
    }

    fun unsign(certificate: Certificate): Boolean {
        val h = hash(certificate)

        return when {
            certificate.signatureHigh <= BigInteger.ZERO -> false
            certificate.signatureHigh >= modulo -> false
            certificate.signatureLow <= BigInteger.ZERO -> false
            certificate.signatureLow >= lowModulo -> false
            else -> {
                val firstValue = result.modPow(certificate.signatureHigh, modulo)
                val secondValue = certificate.signatureHigh.modPow(certificate.signatureLow, modulo)
                val thirdValue = base.modPow(h, modulo)

                firstValue * secondValue % modulo == thirdValue
            }
        }
    }

    companion object {
        val POWER: BigInteger = BigInteger.valueOf(1000000007)
    }

}
