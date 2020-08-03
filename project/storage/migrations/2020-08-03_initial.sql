create schema if not exists stage;

create table if not exists stage.transactions_fct (id_transaction     integer     not null,
                                                   id_account         integer     not null,
                                                   transaction_type   varchar(8),
                                                   transaction_date   date        not null,
                                                   transaction_amount numeric     not null);

create index transactions_fct_acc on stage.transactions_fct (id_account, transaction_date);

create table if not exists stage.accounts_dim (id_account   numeric not null,
                                               id_person    numeric not null,
                                               account_type varchar(16));

create unique index accounts_dim_person_acc on stage.accounts_dim (id_account, id_person);

create table if not exists stage.persons_dim (id_person    integer not null,
                                              name         varchar(128),
                                              surname      varchar(128),
                                              zip          varchar(16),
                                              city         varchar(64),
                                              country      varchar(64),
                                              email        varchar(512),
                                              phone_number varchar(16),
                                              birth_date   date);

create unique index persons_dim_pk on stage.persons_dim
(id_person);

create schema if not exists data_mart;

create or replace view data_mart.transction_m_agg
    as
    with
         list_of_dates
         as (select m.month,
                    p.id_person
             from  (select to_char(
                               generate_series(
                                   date'2020-02-01',
                                   date'2020-06-01',
                                   '1 month'),
                               'mm.yyyy') as month) m
             inner join (select 1234 as id_person
                         union all
                         select 345 as id_person) p
                     on 1 = 1),
        transactions_agg
        as (select per.id_person,
                   to_char(trn.transaction_date, 'mm.yyyy') as month,
                   round(
                       coalesce(
                           sum(transaction_amount), 0),
                       4) as sum_of_transactions
            from   stage.transactions_fct trn
            inner join stage.accounts_dim acc
                    on acc.id_account = trn.id_account
            inner join stage.persons_dim per
                    on per.id_person = acc.id_person
            where  per.id_person in (345,
                                     1234) and
                   trn.transaction_date between date'2020-02-15' and
                                                date'2020-06-06'
            group by per.id_person,
                     to_char(trn.transaction_date, 'mm.yyyy'))
        select lst.id_person,
               lst.month,
               coalesce(
                   trn.sum_of_transactions,
                   0) as sum_of_transactions
        from   list_of_dates lst
        left outer join transactions_agg trn
                     on lst.month = trn.month and
                        lst.id_person = trn.id_person
        order by lst.id_person desc,
                 trn.month;
