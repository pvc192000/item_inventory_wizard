-- Table: public.manager

-- DROP TABLE public.manager;

CREATE TABLE public.manager
(
    manager_id integer NOT NULL,
    name character varying[] COLLATE pg_catalog."default" NOT NULL,
    email character varying[] COLLATE pg_catalog."default" NOT NULL,
    phone character varying[] COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT manager_pkey PRIMARY KEY (manager_id)
)

TABLESPACE pg_default;

ALTER TABLE public.manager
    OWNER to postgres;



-- Table: public.customer

-- DROP TABLE public.customer;

CREATE TABLE public.customer
(
    customer_id integer NOT NULL,
    name character varying[] COLLATE pg_catalog."default" NOT NULL,
    email character varying[] COLLATE pg_catalog."default" NOT NULL,
    phone character varying[] COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT customer_pkey PRIMARY KEY (customer_id)
)

TABLESPACE pg_default;

ALTER TABLE public.customer
    OWNER to postgres;


-- Table: public.item

-- DROP TABLE public.item;

CREATE TABLE public.item
(
    item_id integer NOT NULL,
    name character varying[] COLLATE pg_catalog."default" NOT NULL,
    price real NOT NULL,
    quantity integer NOT NULL,
    available_by date NOT NULL,
    CONSTRAINT item_pkey PRIMARY KEY (item_id)
)

TABLESPACE pg_default;

ALTER TABLE public.item
    OWNER to postgres;


-- Table: public.order_from

-- DROP TABLE public.order_from;

CREATE TABLE public.order_from
(
    manager_id integer NOT NULL,
    supplier_id integer NOT NULL,
    order_id integer NOT NULL,
    quantity integer NOT NULL,
    item_id integer NOT NULL,
    order_date date NOT NULL,
    CONSTRAINT item_id FOREIGN KEY (item_id)
        REFERENCES public.item (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT manager_id FOREIGN KEY (manager_id)
        REFERENCES public.manager (manager_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT supplier_id FOREIGN KEY (supplier_id)
        REFERENCES public.supplier (supplier_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.order_from
    OWNER to postgres;



-- Table: public.purchase

-- DROP TABLE public.purchase;

CREATE TABLE public.purchase
(
    purchase_date date NOT NULL,
    quantity integer NOT NULL,
    customer_id integer NOT NULL,
    item_id integer NOT NULL,
    CONSTRAINT customer_id FOREIGN KEY (customer_id)
        REFERENCES public.customer (customer_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT item_id FOREIGN KEY (item_id)
        REFERENCES public.item (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.purchase
    OWNER to postgres;



-- Table: public.staff

-- DROP TABLE public.staff;

CREATE TABLE public.staff
(
    staff_id integer NOT NULL,
    name character varying[] COLLATE pg_catalog."default" NOT NULL,
    email character varying[] COLLATE pg_catalog."default" NOT NULL,
    phone character varying[] COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT staff_pkey PRIMARY KEY (staff_id)
)

TABLESPACE pg_default;

ALTER TABLE public.staff
    OWNER to postgres;




-- Table: public.supplied_by

-- DROP TABLE public.supplied_by;

CREATE TABLE public.supplied_by
(
    item_id integer NOT NULL,
    supplier_id integer NOT NULL,
    CONSTRAINT item_id FOREIGN KEY (item_id)
        REFERENCES public.item (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT supplier_id FOREIGN KEY (supplier_id)
        REFERENCES public.supplier (supplier_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.supplied_by
    OWNER to postgres;




-- Table: public.supplier

-- DROP TABLE public.supplier;

CREATE TABLE public.supplier
(
    supplier_id integer NOT NULL,
    name character varying[] COLLATE pg_catalog."default" NOT NULL,
    email character varying[] COLLATE pg_catalog."default" NOT NULL,
    phone character varying[] COLLATE pg_catalog."default" NOT NULL,
    avg_delivery_time integer NOT NULL,
    CONSTRAINT supplier_pkey PRIMARY KEY (supplier_id)
)

TABLESPACE pg_default;

ALTER TABLE public.supplier
    OWNER to postgres;






