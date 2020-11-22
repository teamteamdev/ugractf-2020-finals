package ru.ugra.mydocs.security

import ru.ugra.mydocs.certs.Certificate
import ru.ugra.mydocs.certs.ExtendedCertificate
import java.math.BigInteger
import java.security.SecureRandom

object Challenger {
    private val rnd: SecureRandom = SecureRandom()

    fun challenge(): BigInteger {
        return BigInteger.probablePrime(18, rnd)
    }

    fun checkChallenge(certificate: Certificate, chall: BigInteger, high: BigInteger, low: BigInteger): Boolean {
        val lowModulo = certificate.modulo - BigInteger.ONE

        return when {
            high <= BigInteger.ZERO -> false
            high >= certificate.modulo -> false
            low <= BigInteger.ZERO -> false
            low >= lowModulo -> false
            else -> {
                val firstValue = certificate.result.modPow(high, certificate.modulo)
                val secondValue = high.modPow(low, certificate.modulo)
                val thirdValue = certificate.base.modPow(chall, certificate.modulo)

                firstValue * secondValue % certificate.modulo == thirdValue
            }
        }
    }

    fun newCert(password: String): ExtendedCertificate {
        val prime = BigInteger.probablePrime(36, rnd)
        val prime1 = BigInteger.TWO
        val prime2 = prime / BigInteger.TWO
        val lowPrime = prime - BigInteger.ONE
        while (true) {
            val coprime = BigInteger(prime.bitLength(), rnd)

            if (coprime <= BigInteger.ONE || coprime >= lowPrime)
                continue

            if (coprime.modPow(prime1, prime) == BigInteger.ONE)
                continue

            if (coprime.modPow(prime2, prime) == BigInteger.ONE)
                continue

            var exponent: BigInteger
            do {
                exponent = BigInteger(prime.bitLength(), rnd)

                if (exponent <= BigInteger.ONE || exponent >= lowPrime)
                    continue

                if (exponent.gcd(lowPrime) != BigInteger.ONE)
                    continue
            } while (false);

            val result = coprime.modPow(exponent, prime)

            return ExtendedCertificate(
                coprime,
                prime,
                result,
                exponent,
                password
            )
        }
    }
}
