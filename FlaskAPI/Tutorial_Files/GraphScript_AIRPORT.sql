-- https://www.youtube.com/watch?v=PcFzL3ACS7U
-- https://github.com/saphanaacademy/SAPHANACloud/blob/master/travel_graph.sql
-- CHEAT SHEET: https://help.sap.com/viewer/4fe29514fd584807ac9f2a04f6754767/2.0.03/en-US/20d7fd287519101480afbce1b997e4b9.html



-- ----------------- route exists??
-- CREATE PROCEDURE "DBADMIN"."SP_TravelPossible"(
-- 		IN AIRPORTCODEORIGIN NVARCHAR(3), --import
-- 		IN AIRPORTCODEDESTINATION VARCHAR(3), --import
-- 		OUT isPossible BOOLEAN
-- 	)
	
-- 	LANGUAGE GRAPH READS SQL DATA AS
-- 		BEGIN
-- 			Graph g = Graph("DBADMIN", "FLIGHTS");
-- 			Vertex sourceVertex = Vertex(:g, :AIRPORTCODEORIGIN);
-- 			Vertex targetVertex = Vertex(:g, :AIRPORTCODEDESTINATION);
-- 			isPossible = IS_REACHABLE(:g, :sourceVertex, :targetVertex);
-- 		END
-- ;

-- CALL "DBADMIN"."SP_TravelPossible"('NTE', 'PDX', ?);


-------------------shortest path; will return a table, so we'll first create a table type

-- DROP TYPE "DBADMIN"."TT_TripRouting"; -
-- CREATE TYPE "DBADMIN"."TT_TripRouting" AS TABLE (
-- 	"segment" BIGINT, 
-- 	"airportCodeOrigin" NVARCHAR(3),
-- 	"airportCodeDestination" NVARCHAR(3), 
-- 	"airlineName" NVARCHAR(100),
-- 	"distance" INTEGER, 
-- 	"duration" INTEGER
-- );

--create procedure now
-- CREATE PROCEDURE "DBADMIN"."SP_TripRouting"(
-- 		IN AIRPORTCODEORIGIN NVARCHAR(3), --import
-- 		IN AIRPORTCODEDESTINATION VARCHAR(3), --import
-- 		OUT TOTALSEGMENTS BIGINT, 
-- 		OUT TOTALDISTANCE INTEGER, 
-- 		OUT TOTALDURATION INTEGER, 
-- 		OUT ROUTING "DBADMIN"."TT_TripRouting"
-- 	)
	
-- 	LANGUAGE GRAPH READS SQL DATA AS
-- 		BEGIN
-- 			Graph g = Graph("DBADMIN", "FLIGHTS");
-- 			Vertex sourceVertex = Vertex(:g, :AIRPORTCODEORIGIN);
-- 			Vertex targetVertex = Vertex(:g, :AIRPORTCODEDESTINATION);
-- 			WeightedPath<BIGINT> p = SHORTEST_PATH(:g, :sourceVertex, :targetVertex);
-- 			TOTALSEGMENTS = Length(:p);
-- 			TOTALDISTANCE = 0;
-- 			TOTALDURATION = 0;
-- 			FOREACH e IN Edges(:p){
-- 				TOTALDISTANCE  = :TOTALDISTANCE + :e."DISTANCE";
-- 				TOTALDURATION = :TOTALDURATION + :e."DURATION";
-- 			}
-- 			ROUTING = SELECT :segment, :e."AIRPORTCODEORIGIN", :e."AIRPORTCODEDESTINATION", :e."AIRLINENAME", :e."DISTANCE", :e."DURATION" FOREACH e in Edges(:p) WITH ORDINALITY AS segment;
-- 		END
-- ;

-- CALL "DBADMIN"."SP_TripRouting"('NTE', 'PDX', ?, ?, ?, ?);







