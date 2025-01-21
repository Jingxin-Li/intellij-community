plugins {
    id("org.jetbrains.intellij")
    java
}

dependencies {
    implementation(project(":platform:core-api"))
    implementation(project(":platform:analysis-api"))
    implementation(project(":platform:core-impl"))
}

intellij {
    version.set("2023.3")
    type.set("IC")
    plugins.set(listOf("java"))
}
