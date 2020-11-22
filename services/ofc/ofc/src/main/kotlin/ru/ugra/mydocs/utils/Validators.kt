package ru.ugra.mydocs.utils

fun isEnum(s: String): Boolean {
    return s.matches(Regex("^\\d{13}$"))
}

fun validate(b: Boolean?): Boolean? = when (b) {
    true -> true
    else -> null
}
