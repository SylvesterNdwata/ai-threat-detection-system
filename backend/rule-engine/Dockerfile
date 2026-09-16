FROM maven:3.9-eclipse-temurin-11 AS build

WORKDIR /build

COPY pom.xml .
RUN mvn dependency:go-offline

COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:11-jre-alpine

WORKDIR /app

COPY --from=build /build/target/rule-engine-1.0-SNAPSHOT.jar app.jar

CMD ["java", "-jar", "app.jar"]