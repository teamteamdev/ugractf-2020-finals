package ru.ugra.mydocs.certs

import net.spy.memcached.AddrUtil
import net.spy.memcached.ConnectionFactoryBuilder
import net.spy.memcached.MemcachedClient

class PkiStorage {
    private val mc = MemcachedClient(
        ConnectionFactoryBuilder()
            .setProtocol(ConnectionFactoryBuilder.Protocol.BINARY)
            .build(),
        AddrUtil.getAddresses("mc:11211")
    )

    fun get(enum: Long): Certificate? {
        return mc.get("$enum.Certificate")?.let { Certificate.unserialize(it as String) }
    }

    fun put(enum: Long, info: Certificated) {
        mc.set("$enum.${info.javaClass.simpleName}", 0, info.serialize())
    }
}
