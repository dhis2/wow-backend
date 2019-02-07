# JPA criteria query in DHIS2

#### 1. Overview
From 2.31, Hibernate Native API is replaced by JPA Criteria Query. The old hibernate Restriction/Criteria is deprecated. 
Known issues : 
*  We are still using hibernate xml mapping file .hbm, so if we map a compound primary key then JPA Criteria API won't be able to find the attributes belong to that compound ID, For example:

          <composite-id>
                  <key-many-to-one name="programStageInstance" class="org.hisp.dhis.program.ProgramStageInstance"
                    column="programstageinstanceid" foreign-key="fk_entityinstancedatavalue_programstageinstanceid" />
                  <key-many-to-one name="dataElement" class="org.hisp.dhis.dataelement.DataElement" column="dataelementid"
                    foreign-key="fk_entityinstancedatavalue_dataelementid" />
            </composite-id>

    This will fail as JPA can't find the property dataElement of the object TrackedEntityDataValue.

        CriteriaBuilder builder = getCriteriaBuilder();
        return getList( builder, newJpaParameters()
            .addPredicate( root -> builder.equal( root.get( "dataElement" ), dataElement ) ) );

    In this case we need to use the HQL query. 

        String hql = "from TrackedEntityDataValue tv where tv.dataElement =:dataElement";
        return getList( getQuery( hql ).setParameter( "dataElement", dataElement ) );

    So for new objects that have Compound primary key, we must use an ID Java class.
* For now, we have only applied the JPA Criteria Query API, but not fully converted from Hibernate configuration to JPA's configuration such as persistence.xml and entity annotation mapping. Therefore,  we can't use EntityManager and its method. We also can't use JPQL .

#### 2. Todo list
For DHIS2 to fully support JPA specification, below things need to be done.
- Apply JPA Criteria Query for CriteriaQueryEngine and related classes
- Convert hibernate xml mapping to jpa entity annotation mapping
- Convert HibernateConfigurationProvider to JPA's persistence.xml so that we can fully use JPA EntityManager.

#### 3.  Some of the code samples using JPA criteria query inside DHIS2
Note that JPA Criteria Query is a bit complicated, so we have implemented some common generic methods in **HibernateGenericStore** and **HibernateIdentifiableObjectStore**.

- Basic get object method 

        CriteriaBuilder builder = getCriteriaBuilder();
        return getList( builder, newJpaParameters()
            .addPredicate( root -> builder.equal( root.get( "program" ), program ) ) );

- Search String using ilike

        return getList( builder, newJpaParameters()
            .addPredicate( root -> builder.equal( root.get( "program" ), program ) )
            .addPredicate( root -> JpaUtils.stringPredicate( builder, root.get( "name" ), "%" + key + "%", JpaUtils.StringSearchMode.LIKE, false ) )
            .addOrder( root -> builder.asc( root.get( "name" ) ) ) );

- Search Object with compound primary key: need to use an Object to compare with root, instead of comparing each properties.

        CriteriaBuilder builder = getCriteriaBuilder();
        return getSingleResult( builder, newJpaParameters()
            .addPredicate( root -> builder.equal( root, new CompleteDataSetRegistration( dataSet, storedPeriod, source, attributeOptionCombo ) ) ) );

- Count
    
    * Explicit count expression
        
            return count( builder, newJpaParameters()
            .addPredicate( root -> builder.greaterThanOrEqualTo( root.get( "lastUpdated" ), time ) )
            .count( root -> builder.countDistinct( root ) ) );

    * Implicit count expression: count on root, default distinct = false
         
            return count( builder, newJpaParameters()
            .addPredicate( root -> parseFilter( builder, root, query.getFilters() ) )
            .setUseDistinct( true ) )

- Conjunction 
    
        return getList( builder, newJpaParameters()
        .addPredicate( root -> builder.and(
            builder.equal( root.get( "entityInstance" ), entityInstance ),
            builder.equal( root.join( "attribute" ).get( "program" ), program ) ) ) );

- Using Join
    
        CriteriaBuilder builder = getCriteriaBuilder();
         JpaQueryParameters<CategoryOptionGroup> parameters = newJpaParameters()
        .addPredicates( getSharingPredicates( builder ) )
        .addPredicate( root -> {
            Join<Object, Object> groupSets = root.join( "groupSets" );
            return builder.or( builder.equal( groupSets.get( "id" ) , groupSet.getId() ),
                                builder.isNull( groupSets.get( "id" ) ) );
        });
        return getList( builder, parameters );

- Get latest object 

        return getSingleResult( builder, newJpaParameters()
            .addOrder( root -> builder.desc( root.get( "created" ) ) )
            .setMaxResults( 1 )
            .setCachable( false ) );

- Get objects with data sharing applied 
    
        CriteriaBuilder builder = getCriteriaBuilder();
        JpaQueryParameters<T> parameters = new JpaQueryParameters<T>()
                .addPredicates( getDataSharingPredicates( builder, AclService.LIKE_READ_DATA ) );

        return getList( builder, parameters );

- Get objects with metadata sharing applied

        CriteriaBuilder builder = getCriteriaBuilder();
        return getList( builder, new JpaQueryParameters<T>().addPredicates( getSharingPredicates( builder ) ) );

- Using HQL query 

        String hql = "select dv from DataValue dv  where dv.dataElement =:dataElement and dv.period =:period and dv.deleted = false  " +
            "and dv.attributeOptionCombo =:attributeOptionCombo and dv.categoryOptionCombo =:categoryOptionCombo and dv.source =:source ";
        return getSingleResult( getQuery( hql )
            .setParameter( "dataElement", dataElement )
            .setParameter( "period", storedPeriod )
            .setParameter( "source", source )
            .setParameter( "attributeOptionCombo", attributeOptionCombo )
            .setParameter( "categoryOptionCombo", categoryOptionCombo ) );
