
### JPA criteria query in DHIS2
From 2.31, Hibernate Native API is replaced by JPA Criteria Query. The old hibernate Restriction/Criteria is deprecated. 

As the native JPA Criteria Query is a bit complicated, we have implemented some common generic methods in **HibernateGenericStore** and **HibernateIdentifiableObjectStore**. 

Some known issues : 

*  We are still using hibernate xml mapping file .hbm, so if we use a compound primary key JPA Criteria API won't be able to find they attributes belong to that compound mapping, For example:

          <composite-id>
                  <key-many-to-one name="programStageInstance" class="org.hisp.dhis.program.ProgramStageInstance"
                    column="programstageinstanceid" foreign-key="fk_entityinstancedatavalue_programstageinstanceid" />
                  <key-many-to-one name="dataElement" class="org.hisp.dhis.dataelement.DataElement" column="dataelementid"
                    foreign-key="fk_entityinstancedatavalue_dataelementid" />
            </composite-id>


    In this case we need to use the HQL query. So for new objects that have Compound primary key, we must create an ID java class for it.

#### Below are some of the code samples using JPA criteria query inside DHIS2: 

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

- Get objects with data/metadata sharing applied 
    
        CriteriaBuilder builder = getCriteriaBuilder();
        JpaQueryParameters<T> parameters = new JpaQueryParameters<T>()
                .addPredicates( getDataSharingPredicates( builder, AclService.LIKE_READ_DATA ) );

        return getList( builder, parameters );

- Get objects with metadata sharing applied

        CriteriaBuilder builder = getCriteriaBuilder();
        return getList( builder, new JpaQueryParameters<T>().addPredicates( getSharingPredicates( builder ) ) );
