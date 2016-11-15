--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: mytable; Type: TABLE; Schema: public; Owner: scailer
--

CREATE TABLE mytable (
    id bigint NOT NULL,
    title character varying(255) DEFAULT ''::character varying
);


ALTER TABLE mytable OWNER TO scailer;

--
-- Name: mytable_id_seq; Type: SEQUENCE; Schema: public; Owner: scailer
--

CREATE SEQUENCE mytable_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mytable_id_seq OWNER TO scailer;


INSERT INTO mytable(id, title) VALUES (1, 'a');
INSERT INTO mytable(id, title) VALUES (2, 'b');
INSERT INTO mytable(id, title) VALUES (3, 'c');

--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

