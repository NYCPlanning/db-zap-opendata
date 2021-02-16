CREATE TABLE dcp_project (
    dcp_projectid uuid PRIMARY KEY,
    createdon timestamp without time zone,
    createdby uuid,
    modifiedon timestamp without time zone,
    modifiedby uuid,
    createdonbehalfby uuid,
    modifiedonbehalfby uuid,
    ownerid uuid,
    ownerid$type character varying(255),
    owningbusinessunit uuid,
    owninguser uuid,
    owningteam uuid,
    statecode character varying(256),
    statuscode character varying(256),
    versionnumber bigint,
    importsequencenumber integer,
    overriddencreatedon timestamp without time zone,
    timezoneruleversionnumber integer,
    utcconversiontimezonecode integer,
    dcp_name character varying(50),
    processid uuid,
    stageid uuid,
    traversedpath character varying(1250),
    dcp_acoenumberwn integer,
    dcp_address1 character varying(200),
    dcp_address2 character varying(200),
    dcp_alterationmapnumber character varying(100),
    dcp_anticipatedyearbuilt character varying(4),
    dcp_applicant_customer uuid,
    dcp_applicant_customer$type character varying(255),
    dcp_applicantadministrator_customer uuid,
    dcp_applicantadministrator_customer$type character varying(255),
    dcp_applicantpropertyinterest character varying(256),
    dcp_applicantpropertyinterestname text,
    dcp_applicanttype character varying(256),
    dcp_applicanttypename text,
    dcp_applicationfiled timestamp without time zone,
    dcp_bblindocumentrepository boolean,
    dcp_bblindocumentrepositoryname text,
    dcp_block character varying(100),
    dcp_borough character varying(256),
    dcp_boroughname text,
    dcp_boundingstreets character varying(250),
    dcp_bsanumber character varying(11),
    dcp_bsapermitrequired boolean,
    dcp_bsapermitrequiredname text,
    dcp_buildyear character varying(4),
    dcp_cemplannedcompletiondate timestamp without time zone,
    dcp_ceqragencysignoffrequired boolean,
    dcp_ceqragencysignoffrequiredname text,
    dcp_ceqrcomplexity character varying(256),
    dcp_ceqrcomplexityname text,
    dcp_ceqrfee numeric(12,2),
    dcp_ceqrnumber character varying(11),
    dcp_ceqrtype character varying(256),
    dcp_ceqrtypename text,
    dcp_certificationtargetdate timestamp without time zone,
    dcp_certifiedreferred timestamp without time zone,
    dcp_city character varying(100),
    dcp_citycouncildistrict character varying(256),
    dcp_citycouncildistrictname text,
    dcp_cmplannedcompletiondate timestamp without time zone,
    dcp_communitydistrict character varying(256),
    dcp_communitydistrictname text,
    dcp_communitydistricts character varying(260),
    dcp_cpccalendarnumber integer,
    dcp_cpccalendarnumberprefix character varying(1),
    dcp_cpcdeadline integer,
    dcp_cpcdeadlinestartedon timestamp without time zone,
    dcp_cpcdeadlinestoppedon timestamp without time zone,
    dcp_currentenvironmentalmilestoneownertype character varying(256),
    dcp_currentenvironmentalmilestoneownertypename text,
    dcp_currentenvironmentmilestone uuid,
    dcp_currentmilestone uuid,
    dcp_currentmilestoneownertype character varying(256),
    dcp_currentmilestoneownertypename text,
    dcp_currentprojectstatustrack uuid,
    dcp_dcanumber character varying(11),
    dcp_dcpcontactforprojectapplication uuid,
    dcp_dcptargetcertificationdate timestamp without time zone,
    dcp_decpermitnumber character varying(18),
    dcp_decpermitrequired boolean,
    dcp_decpermitrequiredname text,
    dcp_dredging boolean,
    dcp_dredgingname text,
    dcp_eardfirsttrack boolean,
    dcp_eardfirsttrackname text,
    dcp_easeis character varying(256),
    dcp_easeisname text,
    dcp_energy boolean,
    dcp_energyname text,
    dcp_engineeringcontrols boolean,
    dcp_engineeringcontrolsname text,
    dcp_erdlead uuid,
    dcp_fasttrackindicator boolean,
    dcp_fasttrackindicatorname text,
    dcp_federalledreview boolean,
    dcp_federalledreviewname text,
    dcp_femafloodzonea boolean,
    dcp_femafloodzoneaname text,
    dcp_femafloodzonecoastala boolean,
    dcp_femafloodzonecoastalaname text,
    dcp_femafloodzoneshadedx boolean,
    dcp_femafloodzoneshadedxname text,
    dcp_femafloodzonev boolean,
    dcp_femafloodzonevname text,
    dcp_genericreview boolean,
    dcp_genericreviewname text,
    dcp_greeninfrastructure boolean,
    dcp_greeninfrastructurename text,
    dcp_habitatrestoration boolean,
    dcp_habitatrestorationname text,
    dcp_hiddenprojectmetriccategory character varying(256),
    dcp_hiddenprojectmetriccategoryname text,
    dcp_hiddenprojectmetrictarget character varying(256),
    dcp_hiddenprojectmetrictargetname text,
    dcp_inclusionaryhousingworkforce character varying(256),
    dcp_inclusionaryhousingworkforcename text,
    dcp_incrementalnoofparkingpaces integer,
    dcp_institutionalcontrols boolean,
    dcp_institutionalcontrolsname text,
    dcp_inwaterrecreationalaccess boolean,
    dcp_inwaterrecreationalaccessname text,
    dcp_iscpcdeadlinestartedonoverridden boolean,
    dcp_iscpcdeadlinestartedonoverriddenname text,
    dcp_iscpcdeadlinestoppedonoverridden boolean,
    dcp_iscpcdeadlinestoppedonoverriddenname text,
    dcp_isplannedpostcertenddateoverridden boolean,
    dcp_isplannedpostcertenddateoverriddenname text,
    dcp_ispostcert boolean,
    dcp_ispostcertname text,
    dcp_ispostcertstartdateoverridden boolean,
    dcp_ispostcertstartdateoverriddenname text,
    dcp_isprecertstartdateoverridden boolean,
    dcp_isprecertstartdateoverriddenname text,
    dcp_istargetcertificationdateoverridden boolean,
    dcp_istargetcertificationdateoverriddenname text,
    dcp_jamaicabaywatershedprotectionprogram boolean,
    dcp_jamaicabaywatershedprotectionprogramname text,
    dcp_lastmilestonedate timestamp without time zone,
    dcp_lastprojectmilestone uuid,
    dcp_leadaction uuid,
    dcp_leadactionulurp character varying(10),
    dcp_leadagencyforenvreview uuid,
    dcp_leaddivision character varying(256),
    dcp_leaddivisionname text,
    dcp_leadplanner uuid,
    dcp_leadplannercontactnumber character varying(20),
    dcp_leadplannerphonenumber character varying(64),
    dcp_legaldocumentsrequired boolean,
    dcp_legaldocumentsrequiredname text,
    dcp_letterofresolutionlor boolean,
    dcp_letterofresolutionlorname text,
    dcp_litigations boolean,
    dcp_litigationsname text,
    dcp_lot character varying(100),
    dcp_lpcnumber character varying(8),
    dcp_lpcpermitrequired boolean,
    dcp_lpcpermitrequiredname text,
    dcp_memorandumofagreementmoa boolean,
    dcp_memorandumofagreementmoaname text,
    dcp_metriccategory character varying(256),
    dcp_metriccategoryname text,
    dcp_metriccategorypriority integer,
    dcp_migratedceqrlastupdateddate timestamp without time zone,
    dcp_migratedlastupdateddate timestamp without time zone,
    dcp_mihdushighernumber integer,
    dcp_mihduslowernumber integer,
    dcp_mihworkforce boolean,
    dcp_mihworkforcename text,
    dcp_moecchapter5review boolean,
    dcp_moecchapter5reviewname text,
    dcp_needsintervention boolean,
    dcp_needsinterventionname text,
    dcp_nepareview boolean,
    dcp_nepareviewname text,
    dcp_newcommercialsqft numeric(12,2),
    dcp_newcommunityfacilitysqft numeric(12,2),
    dcp_newindustrialsqft numeric(12,2),
    dcp_nextenvironmentalmilestone uuid,
    dcp_nextlandusemilestone uuid,
    dcp_noofparkingspaces integer,
    dcp_noofvoluntaryaffordabledus integer,
    dcp_numberofnewdwellingunits integer,
    dcp_nydospermitnumber character varying(16),
    dcp_nysdosreviewerlkup uuid,
    dcp_otheragencysignoffrequest boolean,
    dcp_otheragencysignoffrequestname text,
    dcp_parkingspacesapprovedwn integer,
    dcp_phase character varying(100),
    dcp_pier boolean,
    dcp_piername text,
    dcp_pilotstudy boolean,
    dcp_pilotstudyname text,
    dcp_plannedpostcertenddate timestamp without time zone,
    dcp_postalcode character varying(10),
    dcp_postcertstartdate timestamp without time zone,
    dcp_precertstartdate timestamp without time zone,
    dcp_previousactiononsite boolean,
    dcp_previousactiononsitename text,
    dcp_previousactiononsitecomments character varying(250),
    dcp_programmaticagreementpa boolean,
    dcp_programmaticagreementpaname text,
    dcp_projectbrief character varying(500),
    dcp_projectcompleted timestamp without time zone,
    dcp_projectdescription character varying(1500),
    dcp_projectidentificationnumber character varying(10),
    dcp_projectname character varying(50),
    dcp_projectphase character varying(256),
    dcp_projectphasename text,
    dcp_projectstagedate timestamp without time zone,
    dcp_projectstatusdate timestamp without time zone,
    dcp_projecttype character varying(256),
    dcp_projecttypename text,
    dcp_publicspacesqft numeric(12,2),
    dcp_publicstatus character varying(256),
    dcp_publicstatusname text,
    dcp_relatedwrpnumber character varying(100),
    dcp_residentialsqft numeric(12,2),
    dcp_roadandsewerinfrastructure boolean,
    dcp_roadandsewerinfrastructurename text,
    dcp_seqrareview boolean,
    dcp_seqrareviewname text,
    dcp_shorelinework boolean,
    dcp_shorelineworkname text,
    dcp_sischoolseat boolean,
    dcp_sischoolseatname text,
    dcp_sisubdivision boolean,
    dcp_sisubdivisionname text,
    dcp_specialareadesignations boolean,
    dcp_specialareadesignationsname text,
    dcp_specialdistrict uuid,
    dcp_stateledreview boolean,
    dcp_stateledreviewname text,
    dcp_statusdate timestamp without time zone,
    dcp_supplementalreview boolean,
    dcp_supplementalreviewname text,
    dcp_targetcertenddate timestamp without time zone,
    dcp_taxblock character varying(100),
    dcp_terminationeligible boolean,
    dcp_terminationeligiblename text,
    dcp_totalnoofdusinprojecd integer,
    dcp_trdlead uuid,
    dcp_ulurp_nonulurp character varying(256),
    dcp_ulurp_nonulurpname text,
    dcp_ulurpnumber character varying(100),
    dcp_visibility character varying(256),
    dcp_visibilityname text,
    dcp_waterdependentuse boolean,
    dcp_waterdependentusename text,
    dcp_withinformerura boolean,
    dcp_withinformeruraname text,
    dcp_wrpnumber character varying(6),
    dcp_wrpreviewrequired boolean,
    dcp_wrpreviewrequiredname text,
    dcp_zoningmapnumber character varying(256),
    dcp_zoningmapnumbername text,
    dcp_zoningoverride boolean,
    dcp_zoningoverridename text,
    dcp_zrsectionnumber character varying(250),
    emailaddress character varying(100),
    lastonholdtime timestamp without time zone,
    onholdtime integer,
    slaid uuid,
    slainvokedid uuid,
    dcp_cpcdeadlinestatus character varying(4000),
    dcp_currentprojectdaynumber integer,
    dcp_daysonhold integer,
    dcp_daysonhold_date timestamp without time zone,
    dcp_daysonhold_state integer,
    dcp_precertactualduration integer,
    dcp_precertnetnumberofdays integer,
    dcp_precertprojectedtotalnumberofdays integer,
    dcp_applicant_customeridtype character varying(4000),
    dcp_applicant_customername character varying(100),
    dcp_applicant_customeryominame character varying(100),
    dcp_applicantadministrator_customeridtype character varying(4000),
    dcp_applicantadministrator_customername character varying(100),
    dcp_applicantadministrator_customeryominame character varying(100),
    dcp_leadagencyforenvreviewname character varying(100),
    dcp_leadagencyforenvreviewyominame character varying(100),
    dcp_dcpcontactforprojectapplicationname character varying(100),
    dcp_dcpcontactforprojectapplicationyominame character varying(100),
    dcp_nysdosreviewerlkupname character varying(100),
    dcp_nysdosreviewerlkupyominame character varying(100),
    dcp_leadactionname character varying(100),
    dcp_currentmilestonename character varying(100),
    dcp_lastprojectmilestonename character varying(100),
    dcp_nextenvironmentalmilestonename character varying(100),
    dcp_nextlandusemilestonename character varying(100),
    dcp_specialdistrictname character varying(100),
    dcp_currentenvironmentmilestonename character varying(100),
    dcp_erdleadname character varying(100),
    dcp_erdleadyominame character varying(100),
    dcp_leadplannername character varying(100),
    dcp_leadplanneryominame character varying(100),
    dcp_trdleadname character varying(100),
    dcp_trdleadyominame character varying(100),
    dcp_currentprojectstatustrackname character varying(100),
    dcp_validatedcommunitydistricts character varying(400),
    dcp_bprmilestone uuid,
    dcp_cpcdeadlinedate timestamp without time zone,
    dcp_bprmilestonename character varying(100),
    dcp_bimonthlyprocess character varying(50),
    dcp_wpwpriority character varying(50),
    dcp_100percentaffordable boolean,
    dcp_100percentaffordablename text,
    dcp_affordablehousing boolean,
    dcp_affordablehousingname text,
    dcp_agencypriorityranking character varying(256),
    dcp_agencypriorityrankingname text,
    dcp_createmodifycommercialoverlay boolean,
    dcp_createmodifycommercialoverlayname text,
    dcp_createmodifycommunityfacilitylargescale boolean,
    dcp_createmodifycommunityfacilitylargescalename text,
    dcp_createmodifyedesignation boolean,
    dcp_createmodifyedesignationname text,
    dcp_createmodifyfresharea boolean,
    dcp_createmodifyfreshareaname text,
    dcp_createmodifygeneraldevelopmentlargescale boolean,
    dcp_createmodifygeneraldevelopmentlargescalename text,
    dcp_createmodifyjointliveworkquartersforartis boolean,
    dcp_createmodifyjointliveworkquartersforartisname text,
    dcp_createmodifylandmark boolean,
    dcp_createmodifylandmarkname text,
    dcp_createmodifymandatoryinclusionaryhousinga boolean,
    dcp_createmodifymandatoryinclusionaryhousinganame text,
    dcp_createmodifymihareadeepaffordabilityoptio boolean,
    dcp_createmodifymihareadeepaffordabilityoptioname text,
    dcp_createmodifymihareaoption1 boolean,
    dcp_createmodifymihareaoption1name text,
    dcp_createmodifymihareaoption2 boolean,
    dcp_createmodifymihareaoption2name text,
    dcp_createmodifymihareaworkforceoption boolean,
    dcp_createmodifymihareaworkforceoptionname text,
    dcp_createmodifyprivatelyownedpublicspace boolean,
    dcp_createmodifyprivatelyownedpublicspacename text,
    dcp_createmodifypubliclyaccessiblewaterfronts boolean,
    dcp_createmodifypubliclyaccessiblewaterfrontsname text,
    dcp_createmodifypublicopenspace boolean,
    dcp_createmodifypublicopenspacename text,
    dcp_createmodifypublicpark boolean,
    dcp_createmodifypublicparkname text,
    dcp_createmodifyresidentialdevelopmentlargesc boolean,
    dcp_createmodifyresidentialdevelopmentlargescname text,
    dcp_createmodifyspecialmixedusedistrictmx boolean,
    dcp_createmodifyspecialmixedusedistrictmxname text,
    dcp_createmodifyspecialnaturalresourcedistric boolean,
    dcp_createmodifyspecialnaturalresourcedistricname text,
    dcp_createmodifytransportationimprovement boolean,
    dcp_createmodifytransportationimprovementname text,
    dcp_createmodifywaterfrontaccessplanwap boolean,
    dcp_createmodifywaterfrontaccessplanwapname text,
    dcp_createmodifywaterfrontpublicaccessarea boolean,
    dcp_createmodifywaterfrontpublicaccessareaname text,
    dcp_currentzoningdistrict character varying(30),
    dcp_developmentorimprovementofaschool boolean,
    dcp_developmentorimprovementofaschoolname text,
    dcp_developmentorimprovementofsupportivehousi boolean,
    dcp_developmentorimprovementofsupportivehousiname text,
    dcp_documentrepository character varying(500),
    dcp_eardtechreviewrequired boolean,
    dcp_eardtechreviewrequiredname text,
    dcp_heipinvolvement boolean,
    dcp_heipinvolvementname text,
    dcp_heipstaffcapacity character varying(256),
    dcp_heipstaffcapacityname text,
    dcp_leadagency uuid,
    dcp_majormodificationtoapreviouslyapprovedact boolean,
    dcp_majormodificationtoapreviouslyapprovedactname text,
    dcp_minormodificationtoapreviouslyapprovedact boolean,
    dcp_minormodificationtoapreviouslyapprovedactname text,
    dcp_proposedzoningdistrict character varying(30),
    dcp_publicfacility boolean,
    dcp_publicfacilityname text,
    dcp_relatedboardofstandardsandappealsapproval boolean,
    dcp_relatedboardofstandardsandappealsapprovalname text,
    dcp_requireslandmarkpreservationcommissionapp boolean,
    dcp_requireslandmarkpreservationcommissionappname text,
    dcp_requirespublicdesigncommissionapproval boolean,
    dcp_requirespublicdesigncommissionapprovalname text,
    dcp_restrictivedeclarationmodification boolean,
    dcp_restrictivedeclarationmodificationname text,
    dcp_seniorhousing boolean,
    dcp_seniorhousingname text,
    dcp_subjecttojointinterestareajiareview boolean,
    dcp_subjecttojointinterestareajiareviewname text,
    dcp_substantialcomplianceofaprevapprovedactio boolean,
    dcp_substantialcomplianceofaprevapprovedactioname text,
    dcp_transferofdevelopmentrights boolean,
    dcp_transferofdevelopmentrightsname text,
    dcp_transportationinvolvement boolean,
    dcp_transportationinvolvementname text,
    dcp_transportationstaffcapacity character varying(256),
    dcp_transportationstaffcapacityname text,
    dcp_urbandesigninvolvement boolean,
    dcp_urbandesigninvolvementname text,
    dcp_urbandesignstaffcapacity character varying(256),
    dcp_urbandesignstaffcapacityname text,
    dcp_voluntaryinclusionaryhousing boolean,
    dcp_voluntaryinclusionaryhousingname text,
    dcp_waterfrontblockorlotnonwapnonwpaa boolean,
    dcp_waterfrontblockorlotnonwapnonwpaaname text,
    dcp_waterfrontinvolvement boolean,
    dcp_waterfrontinvolvementname text,
    dcp_waterfrontstaffcapacity character varying(256),
    dcp_waterfrontstaffcapacityname text,
    dcp_withincurrentorformerurbanrenewalarea boolean,
    dcp_withincurrentorformerurbanrenewalareaname text,
    dcp_withinindustrialbusinesszone boolean,
    dcp_withinindustrialbusinesszonename text,
    dcp_withinoradjacenttohistoricdistrict boolean,
    dcp_withinoradjacenttohistoricdistrictname text,
    dcp_zoninginvolvement boolean,
    dcp_zoninginvolvementname text,
    dcp_zoningstaffcapacity character varying(256),
    dcp_zoningstaffcapacityname text,
    dcp_leadagencyname character varying(100),
    dcp_leadagencyyominame character varying(100),
    dcp_sharepointabsoluteurl character varying(2000),
    dcp_spabsoluteurl character varying(2000),
    dcp_currentprecertonholddays integer,
    dcp_currentstatuscounter integer,
    dcp_totalprecertonholddays integer,
    dcp_totalprecertonholddays_date timestamp without time zone,
    dcp_totalprecertonholddays_state integer,
    dcp_publicvisibilitydate timestamp without time zone,
    dcp_ulurpearliestpossiblecertificationdate timestamp without time zone
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX "PK_dcp_project" ON dcp_project(dcp_projectid uuid_ops);
CREATE INDEX dcp_projectid_idx ON dcp_project(dcp_projectid uuid_ops);