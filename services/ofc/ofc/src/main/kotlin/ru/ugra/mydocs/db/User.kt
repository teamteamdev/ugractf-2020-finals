package ru.ugra.mydocs.db

import org.bson.Document
import org.bson.types.ObjectId

data class User(
    val enum: Long,
    val codeword: String
) {
    var id: ObjectId? = null

    fun toDocument(): Document {
        return Document().apply {
            append("enum", enum)
            append("codeword", codeword)
            val objectId = id ?: return@apply
            append("_id", objectId)
        }
    }

    companion object {
        fun fromDocument(obj: Document): User {
            return User(
                obj["enum"] as Long,
                obj["codeword"] as String
            ).also { it.id = obj["_id"] as ObjectId }
        }
    }
}
