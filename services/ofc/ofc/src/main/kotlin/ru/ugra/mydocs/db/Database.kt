package ru.ugra.mydocs.db

import com.mongodb.MongoClientSettings
import com.mongodb.ServerAddress
import com.mongodb.client.MongoClients
import com.mongodb.client.MongoDatabase
import com.mongodb.client.model.Filters.eq
import com.mongodb.client.model.Filters.where
import com.mongodb.client.model.Sorts.descending
import ru.ugra.mydocs.utils.isEnum

class Database {
    private val storage: MongoDatabase = MongoClients.create(
        MongoClientSettings.builder()
            .applyToClusterSettings {
                it.hosts(listOf(ServerAddress("db")))
            }
            .build()
    ).getDatabase("db")

    fun hasEnum(enum: String): Boolean {
        val users = storage.getCollection("users")
        if (!isEnum(enum)) throw IllegalArgumentException("enum contains not only digits")
        return users.find(where("""function() { return `$s{this.enum}` === "$enum"; }""")).count() > 0;
    }

    fun save(user: User) {
        val users = storage.getCollection("users")

        val userDocument = user.toDocument().apply {
            append("editedAt", System.currentTimeMillis())
        }

        if (user.id == null) {
            users.insertOne(userDocument)
        } else {
            users.updateOne(eq(user.id), userDocument)
        }
    }

    fun getLatest(): List<User> {
        val users = storage.getCollection("users")

        return users.find()
            .sort(descending("editedAt"))
            .limit(200)
            .toList()
            .map(User.Companion::fromDocument)
    }

    fun getOne(enum: Long): User? {
        val users = storage.getCollection("users")
        return users.find(eq("enum", enum)).first()?.let { User.fromDocument(it) }
    }

    companion object {
        const val s = "$"
    }
}
