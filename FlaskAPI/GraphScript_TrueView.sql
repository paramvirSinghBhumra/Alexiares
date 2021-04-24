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
-- CREATE TYPE "DBADMIN"."TT_OrderEffect" AS TABLE (
-- 	"id" INT, 
-- 	"source_id" NVARCHAR(10), -- Subsystem_id = 1 -> "ssy1" 
-- 	"effectedNode_id" NVARCHAR(10), -- System_id = 1 -> "sy1"
-- 	"orderOfEffect" INT -- 2nd/3rd order effect
-- );

-- create procedure for "Mission" asset (NOT DONE!!!!!) --
-- CREATE PROCEDURE "DBADMIN"."SPECIFIC_Mission"(
-- 	IN sourceID NVARCHAR(10), 
-- 	OUT counter INT,
-- 	OUT effectedNodeID NVARCHAR(10),
-- 	OUT orderEffect INT,
-- 	OUT ROUTING "DBADMIN"."TT_OrderEffect"
-- )
	
-- 	LANGUAGE GRAPH READS SQL DATA AS
-- 		BEGIN
-- 			Graph g = Graph("DBADMIN", "Mission_Graph");
-- 			Vertex sourceVertex = Vertex(:g, :sourceID);
-- 			-- we'll need to add a suffix for each individual type of asset; mission will be "m"
-- 			-- we'll only add nodes in which 'impacts' == true. x -(impacts==true)-> y means x going down will effect y OR y will be effeced by x going offline.
-- 			--ROUTING = SELECT :segment, :e."AIRPORTCODEORIGIN", :e."AIRPORTCODEDESTINATION", :e."AIRLINENAME", :e."DISTANCE", :e."DURATION" FOREACH e in Edges(:p) WITH ORDINALITY AS segment;
-- 		END
-- ;

-- CALL "DBADMIN"."SPECIFIC_Mission"(1, ?,?,?,?);





-- create procedure for "Site" asset -- 

-- create procedure for "System" asset --

-- create procedure for "Subsystem" asset -- 
