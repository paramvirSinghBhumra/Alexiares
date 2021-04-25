-- Adding CMAFB coordinates to "Site" table --
-- UPDATE "DBADMIN"."Site" SET "location" = NEW ST_POINT(38.7445, 104.8461);

-- Added CCAFS to the "Site" table --
-- INSERT INTO "DBADMIN"."Site" VALUES (2, 'CCAFS', new ST_Point(28.4887, 80.5728));

-- Updated values in "System" table --
-- INSERT INTO "DBADMIN"."System" VALUES (5, 'Communications and Infastructure', 2);
-- INSERT INTO "DBADMIN"."System" VALUES (6, 'Missile Warning Center', 2);
-- INSERT INTO "DBADMIN"."System" VALUES (7, 'Radar Sensors', 2);


-- Did the same for all Edge Tables --
-- ALTER TABLE "Subsystem_Edges" ADD FOREIGN KEY ("subsystem_origin_id") REFERENCES "Subsystem" ("id");
-- ALTER TABLE "Subsystem_Edges" ADD FOREIGN KEY ("subsystem_dest_id") REFERENCES "Subsystem" ("id");
 

-- create edge table for Site and Mission tables (example below is for the "Site" table) -- 
-- CREATE TABLE "DBADMIN"."Site_Edges" (
-- 	"id" INTEGER NOT NULL,
-- 	"site_origin_id" INTEGER NOT NULL,
-- 	"site_dest_id" INTEGER NOT NULL, 
-- 	"impacts" BOOLEAN,
	
-- 	PRIMARY KEY (
-- 		"id"
-- 	)
-- );

-- create graphs for both "Mission" and "Site" tables -- 
-- CREATE GRAPH WORKSPACE "Mission_Graph"
--   EDGE TABLE "Mission_Edges"
--     SOURCE COLUMN "mission_origin_id"
--     TARGET COLUMN "mission_dest_id"
--     KEY COLUMN "id"
--   VERTEX TABLE "Mission"
--     KEY COLUMN "id"
-- ;

----------------------------------------------------------------------------------------------------------------------------

-- created table type for "order effect" GraphScript -- 
DROP TYPE "DBADMIN"."TT_OrderEffect";
CREATE TYPE "DBADMIN"."TT_OrderEffect" AS TABLE (
	"effectedNode_id" INT,
	"parentNode_id" INT
);




-- create procedure for "Mission" asset --

-- DROP PROCEDURE "DBADMIN"."SPECIFIC1_Mission";
CREATE PROCEDURE "DBADMIN"."SPECIFIC1_Mission"(
	IN sourceID INT,
	OUT EFFECT "DBADMIN"."TT_OrderEffect"
	
)
	
	LANGUAGE GRAPH READS SQL DATA AS
		BEGIN
			Graph g = Graph("DBADMIN", "Mission_Graph");
			Vertex sourceVertex = Vertex(:g, :sourceID);
			MULTISET<VERTEX> neighbors1 = Neighbors(:g, :sourceVertex, 1,1);
			MULTISET<VERTEX> neighbors2 = Neighbors(:g, :sourceVertex, 2,2);
			EFFECT = SELECT :n."id", :n."id" FOREACH n in :neighbors1;
		
		END;
		
		
-- DROP PROCEDURE "DBADMIN"."SPECIFIC2_Mission";		
CREATE PROCEDURE "DBADMIN"."SPECIFIC2_Mission"(
	IN sourceID INT,
	OUT EFFECT "DBADMIN"."TT_OrderEffect"
)
	LANGUAGE GRAPH READS SQL DATA AS
		BEGIN
			Graph g = Graph("DBADMIN", "Mission_Graph");
			Vertex sourceVertex = Vertex(:g, :sourceID);
			MULTISET<VERTEX> neighbors2 = Neighbors(:g, :sourceVertex, 2,2);
			EFFECT = SELECT :n."id", :n."id" FOREACH n in :neighbors2; -- repeated :n."id" twice to fit in with the standard TableType
		END;
		
		
		

CALL "DBADMIN"."SPECIFIC1_Mission"(1, ?);
CALL "DBADMIN"."SPECIFIC2_Mission"(1 ,?);



-- create procedure for "Site" asset -- 

-- DROP PROCEDURE "DBADMIN"."SPECIFIC1_Site";
CREATE PROCEDURE "DBADMIN"."SPECIFIC1_Site"(
	IN sourceID INT,
	OUT EFFECT "DBADMIN"."TT_OrderEffect"
	
)
	
	LANGUAGE GRAPH READS SQL DATA AS
		BEGIN
			Graph g = Graph("DBADMIN", "Site_Graph");
			Vertex sourceVertex = Vertex(:g, :sourceID);
			MULTISET<VERTEX> neighbors1 = Neighbors(:g, :sourceVertex, 1,1);
			MULTISET<VERTEX> neighbors2 = Neighbors(:g, :sourceVertex, 2,2);
			EFFECT = SELECT :n."id", :n."id" FOREACH n in :neighbors1;
		
		END;
		
		
-- DROP PROCEDURE "DBADMIN"."SPECIFIC2_Site";		
CREATE PROCEDURE "DBADMIN"."SPECIFIC2_Site"(
	IN sourceID INT,
	OUT EFFECT "DBADMIN"."TT_OrderEffect"
	
)
	LANGUAGE GRAPH READS SQL DATA AS
		BEGIN
			Graph g = Graph("DBADMIN", "Site_Graph");
			Vertex sourceVertex = Vertex(:g, :sourceID);
			MULTISET<VERTEX> neighbors2 = Neighbors(:g, :sourceVertex, 2,2);
			EFFECT = SELECT :n."id", :n."id" FOREACH n in :neighbors2; -- repeated :n."id" twice to fit in with the standard TableType
		END;
		
		
		

CALL "DBADMIN"."SPECIFIC1_Site"(1, ?);
CALL "DBADMIN"."SPECIFIC2_Site"(1 ,?);



-- create procedure for "System" asset --

-- DROP PROCEDURE "DBADMIN"."SPECIFIC1_System";
CREATE PROCEDURE "DBADMIN"."SPECIFIC1_System"(
	IN sourceID INT,
	OUT EFFECT "DBADMIN"."TT_OrderEffect"
	
)
	
	LANGUAGE GRAPH READS SQL DATA AS
		BEGIN
			Graph g = Graph("DBADMIN", "Systems_Graph");
			Vertex sourceVertex = Vertex(:g, :sourceID);
			MULTISET<VERTEX> neighbors1 = Neighbors(:g, :sourceVertex, 1,1);
			MULTISET<VERTEX> neighbors2 = Neighbors(:g, :sourceVertex, 2,2);
			EFFECT = SELECT :n."id", :n."Site_id" FOREACH n in :neighbors1;
		
		END;
		
		
-- DROP PROCEDURE "DBADMIN"."SPECIFIC2_System";		
CREATE PROCEDURE "DBADMIN"."SPECIFIC2_System"(
	IN sourceID INT,
	OUT EFFECT "DBADMIN"."TT_OrderEffect"
	
)
	LANGUAGE GRAPH READS SQL DATA AS
		BEGIN
			Graph g = Graph("DBADMIN", "Systems_Graph");
			Vertex sourceVertex = Vertex(:g, :sourceID);
			MULTISET<VERTEX> neighbors2 = Neighbors(:g, :sourceVertex, 2,2);
			EFFECT = SELECT :n."id", :n."Site_id" FOREACH n in :neighbors2; -- repeated :n."id" twice to fit in with the standard TableType
		END;
		
		
		

CALL "DBADMIN"."SPECIFIC1_System"(1, ?);
CALL "DBADMIN"."SPECIFIC2_System"(1 ,?);




-- create procedure for "Subsystem" asset -- 
DROP PROCEDURE "DBADMIN"."SPECIFIC1_Subsystem";
CREATE PROCEDURE "DBADMIN"."SPECIFIC1_Subsystem"(
	IN sourceID INT,
	OUT EFFECT "DBADMIN"."TT_OrderEffect"
	
)
	
	LANGUAGE GRAPH READS SQL DATA AS
		BEGIN
			Graph g = Graph("DBADMIN", "Subsystem_Graph");
			Vertex sourceVertex = Vertex(:g, :sourceID);
			MULTISET<VERTEX> neighbors1 = Neighbors(:g, :sourceVertex, 1,1);
			MULTISET<VERTEX> neighbors2 = Neighbors(:g, :sourceVertex, 2,2);
			EFFECT = SELECT :n."id", :n."System_id" FOREACH n in :neighbors1;
		
		END;
		
		
DROP PROCEDURE "DBADMIN"."SPECIFIC2_Subsystem";		
CREATE PROCEDURE "DBADMIN"."SPECIFIC2_Subsystem"(
	IN sourceID INT,
	OUT EFFECT "DBADMIN"."TT_OrderEffect"
	
)
	LANGUAGE GRAPH READS SQL DATA AS
		BEGIN
			Graph g = Graph("DBADMIN", "Subsystem_Graph");
			Vertex sourceVertex = Vertex(:g, :sourceID);
			MULTISET<VERTEX> neighbors2 = Neighbors(:g, :sourceVertex, 2,2);
			EFFECT = SELECT :n."id", :n."System_id" FOREACH n in :neighbors2; -- repeated :n."id" twice to fit in with the standard TableType
		END;
		
		
		

CALL "DBADMIN"."SPECIFIC1_Subsystem"(1, ?);
CALL "DBADMIN"."SPECIFIC2_Subsystem"(1 ,?);

