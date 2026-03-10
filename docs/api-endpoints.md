\## Relational Database Endpoints (with execution screenshots)



Below are all relational endpoints exposed by the FastAPI backend, each with an execution screenshots.



---


###  Disciplines

#### **GET /disciplines/**
List all disciplines.
![List Disciplines](imgs/disciplines_list.png)

#### **GET /disciplines/{discipline_id}**
Retrieve a specific discipline.
![Get Discipline](imgs/discipline_detail.png)

#### **GET /disciplines/{discipline_id}/programs**
List all programs for a discipline.
![Programs by Discipline](imgs/programs_by_discipline.png)

---

###  Programs

#### **GET /programs/**
List all programs.
![List Programs](imgs/programs_list.png)

#### **GET /programs/{program_stream_id}**
Retrieve a program by stream ID.
![Program by Stream](imgs/program_by_stream.png)

---

###  Schools

#### **GET /schools/**
List all schools.
![List Schools](imgs/schools_list.png)

#### **GET /schools/{school_id}**
Retrieve a specific school.
![Get School](imgs/school_detail.png)

#### **GET /schools/{school_id}/programs**
List all programs offered by a school.
![School Programs](imgs/school_programs.png)

---

###  Sites

#### **GET /sites/**
List all sites.
![List Sites](imgs/sites_list.png)

#### **GET /sites/{site_id}**
Retrieve a specific site.
![Get Site](imgs/site_id.png)

#### **GET /sites/{site_id}/programs**
List all programs associated with a site.
![Site Programs](imgs/site_programs.png)

---

###  Streams

#### **GET /streams/**
List all program streams.
![List Streams](imgs/streams_list.png)
