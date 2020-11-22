package ru.ugra.mydocs.web

import java.math.BigInteger

data class UserSession(
    val enum: Long? = null,
    val challenge: BigInteger? = null
)
