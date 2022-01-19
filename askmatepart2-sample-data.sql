--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Ubuntu 13.5-0ubuntu0.21.04.1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-0ubuntu0.21.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.question_tag DROP CONSTRAINT fk_tag_id;
ALTER TABLE ONLY public.comment DROP CONSTRAINT fk_question_id;
ALTER TABLE ONLY public.question_tag DROP CONSTRAINT fk_question_id;
ALTER TABLE ONLY public.answer DROP CONSTRAINT fk_question_id;
ALTER TABLE ONLY public.comment DROP CONSTRAINT fk_answer_id;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pk;
ALTER TABLE ONLY public.tag DROP CONSTRAINT pk_tag_id;
ALTER TABLE ONLY public.question_tag DROP CONSTRAINT pk_question_tag_id;
ALTER TABLE ONLY public.question DROP CONSTRAINT pk_question_id;
ALTER TABLE ONLY public.comment DROP CONSTRAINT pk_comment_id;
ALTER TABLE ONLY public.answer DROP CONSTRAINT pk_answer_id;
ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.tag ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.question ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.comment ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.answer ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.users_id_seq;
DROP TABLE public.users;
DROP SEQUENCE public.tag_id_seq;
DROP TABLE public.tag;
DROP TABLE public.question_tag;
DROP SEQUENCE public.question_id_seq;
DROP TABLE public.question;
DROP SEQUENCE public.comment_id_seq;
DROP TABLE public.comment;
DROP SEQUENCE public.answer_id_seq;
DROP TABLE public.answer;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer,
    acceptance boolean
);


--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);


--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);


--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


--
-- Name: tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text,
    password text,
    registration text,
    reputation integer
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.answer VALUES (26, '2021-12-22 12:31:00', 0, 14, 'jjnjn', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (25, '2021-12-22 11:56:00', 9, 11, 'hfjksj', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (15, '2021-12-21 22:14:00', 2, 11, 'kk', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (27, '2021-12-22 13:02:00', 0, 11, 'jknjnk', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (1, '2017-04-28 16:49:00', 10, 1, 'You need to use brackets: my_list = []', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (34, '2021-12-23 10:22:00', 0, 1, 'a new answer
', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (2, '2017-04-25 14:42:00', 37, 1, 'Look it up in the Python docs', 'images/image2.jpg', NULL, NULL);
INSERT INTO public.answer VALUES (17, '2021-12-22 10:07:00', 0, 14, 'cejkkcj..kj', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (35, '2021-12-23 16:02:00', 8, 17, 'stuff about your mama', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (30, '2021-12-22 17:55:00', 0, 16, 'ffff', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (36, '2021-12-23 21:41:00', 5, 21, 'fjrognlknvld', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (37, '2021-12-23 21:41:00', 0, 21, 'mamamamammataaaaaaaa', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (38, '2021-12-23 21:41:00', 0, 21, 'bblablabalbalalabla', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (22, '2021-12-22 11:13:00', 1, 13, 'csl;ss', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (20, '2021-12-22 11:12:00', 0, 13, 'cece', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (21, '2021-12-22 11:13:00', 0, 13, 'djsjsl', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (29, '2021-12-22 17:44:00', 0, 16, 'te
', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (19, '2021-12-22 10:12:00', 5, 13, 'efe', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (39, '2021-12-26 19:43:00', 0, 0, 'KLL', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (9, '2021-12-21 19:15:00', 8, 0, 'stuff', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (41, '2022-01-11 21:29:00', 0, 25, 'kuhkjhj', NULL, 1, false);
INSERT INTO public.answer VALUES (32, '2021-12-22 18:38:00', 0, 0, 'ekeek', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (42, '2022-01-11 21:33:00', 0, 27, 'vsvsvs', NULL, 1, false);
INSERT INTO public.answer VALUES (44, '2022-01-17 09:10:00', 0, 28, 'uhoy', NULL, 1, false);
INSERT INTO public.answer VALUES (40, '2022-01-10 20:00:00', 3, 23, '...just google it', NULL, NULL, NULL);
INSERT INTO public.answer VALUES (43, '2022-01-13 17:00:00', 5, 28, 'dunno YES', NULL, 1, true);


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00', NULL, NULL);
INSERT INTO public.comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00', NULL, NULL);
INSERT INTO public.comment VALUES (3, 13, 19, 'jfjklej', '2021-12-22 10:12:00', 0, NULL);
INSERT INTO public.comment VALUES (4, 13, 19, 'jhcjekhck', '2021-12-22 10:24:00', 0, NULL);
INSERT INTO public.comment VALUES (5, 13, 19, 'scs', '2021-12-22 10:25:00', 0, NULL);
INSERT INTO public.comment VALUES (6, 13, 19, 'efef', '2021-12-22 10:29:00', 0, NULL);
INSERT INTO public.comment VALUES (7, NULL, 15, 'jchsjchj', '2021-12-22 11:56:00', 0, NULL);
INSERT INTO public.comment VALUES (8, NULL, 25, 'yuyuiyiu', '2021-12-22 12:14:00', 0, NULL);
INSERT INTO public.comment VALUES (9, NULL, 17, 'bmnbm', '2021-12-22 12:31:00', 0, NULL);
INSERT INTO public.comment VALUES (10, 1, NULL, 'gfg', '2021-12-22 12:43:00', 0, NULL);
INSERT INTO public.comment VALUES (11, 1, NULL, 'gfgffff', '2021-12-22 12:43:00', 0, NULL);
INSERT INTO public.comment VALUES (12, NULL, 15, 'mkll', '2021-12-22 13:02:00', 0, NULL);
INSERT INTO public.comment VALUES (13, 11, NULL, 'bjhbjl.', '2021-12-22 13:03:00', 0, NULL);
INSERT INTO public.comment VALUES (14, 0, NULL, 'ckmclk', '2021-12-22 13:14:00', 0, NULL);
INSERT INTO public.comment VALUES (15, NULL, 9, 'vls vs', '2021-12-22 13:14:00', 0, NULL);
INSERT INTO public.comment VALUES (16, 0, NULL, 'vmslksv', '2021-12-22 13:15:00', 0, NULL);
INSERT INTO public.comment VALUES (17, 0, NULL, 'mhbbn', '2021-12-22 13:29:00', 0, NULL);
INSERT INTO public.comment VALUES (18, NULL, 9, 'jjbmb', '2021-12-22 13:29:00', 0, NULL);
INSERT INTO public.comment VALUES (19, 0, NULL, 'f4kfkl4f', '2021-12-22 14:02:00', 0, NULL);
INSERT INTO public.comment VALUES (20, 14, NULL, 'jnln,m', '2021-12-22 14:08:00', 0, NULL);
INSERT INTO public.comment VALUES (21, NULL, 17, 'kjlkn. lkn.', '2021-12-22 14:08:00', 0, NULL);
INSERT INTO public.comment VALUES (22, NULL, 17, 'jxhjwwjw', '2021-12-22 14:08:00', 0, NULL);
INSERT INTO public.comment VALUES (23, NULL, 26, 'ejhc', '2021-12-22 14:08:00', 0, NULL);
INSERT INTO public.comment VALUES (24, NULL, 17, 'lvnsnvsjhfk', '2021-12-22 14:18:00', 0, NULL);
INSERT INTO public.comment VALUES (25, NULL, 26, ' hewjt hwjkhw
', '2021-12-22 14:18:00', 0, NULL);
INSERT INTO public.comment VALUES (26, 14, NULL, 'gyge jdb', '2021-12-22 14:18:00', 0, NULL);
INSERT INTO public.comment VALUES (27, NULL, 29, 'jygjhg jhg', '2021-12-22 17:44:00', 0, NULL);
INSERT INTO public.comment VALUES (28, 16, NULL, 'yhfyjhgjgh', '2021-12-22 17:44:00', 0, NULL);
INSERT INTO public.comment VALUES (29, NULL, 29, 'vbvb', '2021-12-22 17:45:00', 0, NULL);
INSERT INTO public.comment VALUES (30, 16, NULL, 'hmvn', '2021-12-22 17:45:00', 0, NULL);
INSERT INTO public.comment VALUES (31, 16, NULL, 'ttttt', '2021-12-22 19:12:00', 0, NULL);
INSERT INTO public.comment VALUES (32, NULL, 29, 'gggg', '2021-12-22 19:12:00', 0, NULL);
INSERT INTO public.comment VALUES (33, 1, NULL, 'hjkhkjhj', '2021-12-22 22:26:00', 0, NULL);
INSERT INTO public.comment VALUES (34, NULL, 2, 'khjkhkjhkhk', '2021-12-22 22:26:00', 0, NULL);
INSERT INTO public.comment VALUES (35, 1, NULL, 'it is nice', '2021-12-23 10:21:00', 0, NULL);
INSERT INTO public.comment VALUES (36, NULL, 1, 'answer to comment', '2021-12-23 10:21:00', 0, NULL);
INSERT INTO public.comment VALUES (37, NULL, 36, 'cjehckjkheocw', '2021-12-23 21:41:00', 0, NULL);
INSERT INTO public.comment VALUES (38, 21, NULL, 'dedmekmdekl', '2021-12-23 21:42:00', 0, NULL);
INSERT INTO public.comment VALUES (39, 21, NULL, 'ddm3kmd3kdm3', '2021-12-23 21:42:00', 0, NULL);
INSERT INTO public.comment VALUES (40, 21, NULL, 'vrovronvovuobobovb55ob5ob5owhyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy', '2021-12-23 21:42:00', 0, NULL);
INSERT INTO public.comment VALUES (41, NULL, 40, 'HAHAHAHA', '2022-01-10 20:01:00', 0, NULL);
INSERT INTO public.comment VALUES (42, NULL, 43, 'pwifoi', '2022-01-17 09:12:00', 0, 1);
INSERT INTO public.comment VALUES (43, 28, NULL, 'JJKKJ', '2022-01-17 09:42:00', 0, 1);


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.question VALUES (24, '2022-01-11 14:25:00', 1, 0, 'do you know something about css', 'i don''t please help', '', NULL);
INSERT INTO public.question VALUES (13, '2021-12-22 10:06:00', 21, 0, 'hgfhjvjh', 'kkekflwelekw', '', NULL);
INSERT INTO public.question VALUES (18, '2021-12-22 19:41:00', 0, 0, 'ffs', 'dfafa', '', NULL);
INSERT INTO public.question VALUES (11, '2021-12-21 21:16:00', 43, 3, 'tata', 'tc55', '', NULL);
INSERT INTO public.question VALUES (19, '2021-12-23 10:20:00', 1, 0, 'css use', 'navbar', '', NULL);
INSERT INTO public.question VALUES (17, '2021-12-22 19:41:00', 10, 0, 'hgjkghkjh', 'hjhjkgGjdfgjfdf', '../static/images/Screenshot_from_2021-09-29_08-58-30.png', NULL);
INSERT INTO public.question VALUES (14, '2021-12-22 10:07:00', 18, 1, 'cbehbekh', 'stuff about stuff', '../static/images/Screenshot.jpg', NULL);
INSERT INTO public.question VALUES (15, '2021-12-22 16:54:00', 0, 0, 'wdjkwj', 'dwjhkjw', '', NULL);
INSERT INTO public.question VALUES (16, '2021-12-22 16:54:00', 20, 0, 'ehejhd', 'xnxx', '../static/images/Screenshot_from_2021-09-29_14-44-16.png', NULL);
INSERT INTO public.question VALUES (20, '2021-12-23 10:20:00', 8, 4, 'damage', 'file error', '../static/images/Screenshot_from_2021-09-29_08-58-30.png', NULL);
INSERT INTO public.question VALUES (27, '2022-01-11 21:33:00', 98, 3, 'stuff about stuff and mooore stuff', 'please learn me somtin about this', '', 1);
INSERT INTO public.question VALUES (26, '2022-01-11 14:31:00', 1, 0, 'g4rgpifk;we', 'ifyfhkyuweyhwke', '', 1);
INSERT INTO public.question VALUES (25, '2022-01-11 14:31:00', 6, 0, 'hahkagfj', 'nymamamamammamama', '', 1);
INSERT INTO public.question VALUES (23, '2022-01-10 19:59:00', 27, 3, 'do you know things about html?', 'html is very hard please help me with some tutorials', NULL, NULL);
INSERT INTO public.question VALUES (1, '2017-04-29 09:19:00', 71, 15, 'Wordpress loading multiple jQuery Versions!!!!!!', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();!!!

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', NULL, NULL);
INSERT INTO public.question VALUES (21, '2021-12-23 21:40:00', 21, 7, 'stufff', 'css/html', NULL, NULL);
INSERT INTO public.question VALUES (22, '2021-12-26 19:42:00', 0, 0, 'GFGFG', 'GGFGFHF', NULL, NULL);
INSERT INTO public.question VALUES (0, '2017-04-28 08:29:00', 118, 16, 'How to make lists in Python?KJKJ', 'I am totally new to this, any hints?', NULL, NULL);
INSERT INTO public.question VALUES (28, '2022-01-13 14:12:00', 24, 4, 'stufff', 'moree stuff', '../static/imagesScreenshot_from_2021-09-27_22-26-36.png', 1);


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.question_tag VALUES (0, 1);
INSERT INTO public.question_tag VALUES (1, 3);


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.tag VALUES (1, 'python');
INSERT INTO public.tag VALUES (2, 'sql');
INSERT INTO public.tag VALUES (3, 'css');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users VALUES (1, 'maria@coolcoder.com', '$2b$12$pIhrJSdCcSdy53iFhd/a3.zLfl3NAhNW4ENWUhKu0ZxnbD0HqxM/G', '2022-01-11 11:56', 0);
INSERT INTO public.users VALUES (2, 'elena.ion00@yahoo.com', '$2b$12$zW3MIOnumXNOVm7YCGTe4.vUhj.AH4Y4EGLsEm4LuoiGx/K0e1XKm', '2022-01-13 17:27', 0);
INSERT INTO public.users VALUES (3, 'op@yahoo.com', '$2b$12$yL69BLcG6J5eVEB2fXoe6eUU8TF45ECt8WGLm902PcOwvcusnqH4.', '2022-01-17 10:31', 0);


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.answer_id_seq', 44, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.comment_id_seq', 43, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.question_id_seq', 28, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tag_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: users users_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- PostgreSQL database dump complete
--

