package ru.ugra.mydocs.utils

import java.math.BigInteger

fun positiveMod(a: BigInteger, b: BigInteger): BigInteger {
    val x = a % b
    return when {
        x < BigInteger.ZERO -> x + b
        else -> x
    }
}
