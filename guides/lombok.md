# Project Lombok DHIS2 guide

As of DHIS2 2.34 we now allow usage of [Project Lombok](https://projectlombok.org/) in our code, it does however come with some restrictions.

## IDE setup

To have Lombok function properly in IDEs like Intellij and Eclipse you will have to enable APT (annotation processing tool) and also install a plugin which helps with auto-complete etc, a nice guide for this can be found [here](https://www.baeldung.com/lombok-ide).

Maven already supports APT (through the lombok depdendency), so for CI servers etc no additional setup is needed.

Occasionally IntelliJ tends to get out of sync with lombok and shows errors related to generated code even if setup is correct and compilation works.
In such case use `File` => `Invalidate Caches / Restart...`.

## Allowed annotations

Current we only allow Lombok to be used for simple bean classes (DTOs, parameter classes etc), and we only allow the following annotations.

1. [@Data](https://projectlombok.org/features/Data) (and by implication also [@ToString](https://projectlombok.org/features/ToString) and [@EqualsAndHashCode](https://projectlombok.org/features/EqualsAndHashCode) )
2. [@Value](https://projectlombok.org/features/Value)
3. [@Builder, @Singular](https://projectlombok.org/features/Builder)
4. [@Getter, @Setter](https://projectlombok.org/features/GetterSetter)
5. [@NoArgsConstructor, @RequiredArgsConstructor, @AllArgsConstructor](https://projectlombok.org/features/constructor)
6. [@Accessors(chain=true)](https://projectlombok.org/features/experimental/Accessors)
7. [@With](https://projectlombok.org/features/With)

## Other annotations

Ask in the backend team meeting if you'd like to use any annotation not on the [allowed annotations](#Allowed-annotations) list.

We discourage using [@SneakyThrows](https://projectlombok.org/features/SneakyThrows) even though you might find usages of it in our code.

## Fine Tuning

Be careful when using `@ToString` or `@EqualsAndHashCode` (and by implication also `@Data`) as they by default include all fields. This is mostly a problem for domain objects where circular or very deep graphs would be referenced and effectivly considered in `toString()` and `hashCode()` generated. For that reason such classes often had manually written implementations where certain fields intentionally were left out. The same can be done using `@ToString` or `@EqualsAndHashCode` by annotating the fields with `@ToString.Exclude` or `@EqualsAndHashCode.Exclude`.

## Examples

* Simple DAO + builder class used for Artemis audit persistence, please be aware that this pattern should only be used for simple JDBC objects (and not for JPA) [Audit.java](https://github.com/dhis2/dhis2-core/blob/master/dhis-2/dhis-api/src/main/java/org/hisp/dhis/audit/Audit.java).

* DTO class + builder used for Artemis audit message passing, this example also shows how you can integrate `@JsonPOJOBuilder` (from Jackson) with Lombok builders [Audit.java](https://github.com/dhis2/dhis2-core/blob/master/dhis-2/dhis-support/dhis-support-artemis/src/main/java/org/hisp/dhis/artemis/audit/Audit.java).
