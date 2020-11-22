FROM python:3-alpine

# GOST 34.10-2077
COPY generate_key.py /
RUN sh -c 'python3 generate_key.py > keys'

FROM openjdk:11

# Cache gradle distribution
COPY gradlew /ofc/
COPY gradle /ofc/gradle
WORKDIR /ofc
RUN ./gradlew help

# Cache gradle dependencies
COPY build.gradle gradle.properties settings.gradle /ofc/
RUN ./gradlew getDeps

# Build actual project
COPY . /ofc
RUN ./gradlew fatJar

# Build a small container
FROM openjdk:11
WORKDIR /ofc
COPY --from=0 /keys /keys
COPY --from=1 /ofc/build/libs/ofc-2020.jar /ofc/ofc.jar
EXPOSE 8080
