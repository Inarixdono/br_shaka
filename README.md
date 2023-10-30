# Shaka
Shaka is a tool for automating the data entry processes for Building Resilience's management information system. It started from my most basic concepts about programming, I've been and I'll be upgrading it as more as I learn.
Building Resilience is a project from USAID agency, and its goal is to improve living conditions from orphan and vulnerable children to HIV. It has a service portfolio which goes from doing HIV test and helping HIV+ patients to get their ARTs, to delivering wash materials, food and giving vocational training.
## Usage
* [libreria.py] contains the MIS class, it has all the tools to interact with the system all along the forms, each form may include specific functions which will be used just in there.
*  Running [formulario_06.py] opens services form and fill the necessary fields with the information provided by [servir.csv]. It has explicit waits and a list with beneficiaries who aren't in the project anymore (so it won't mark services to those members), which reduces data entry process from 3 - 5 minutes per form to 30 seconds per form at most.
* [formulario_011.py] is programmed for the adherence form. By default, the form includes conditionals which depending on the answers from the paper form, it skips some questions which are almost always the same. With Shaka and Selenium, depending on the answers, it goes directly to the next question, so you don't have to lose time looking for it. It is on progress and at the moment it has to be filled by user input, but sooner than later it will work as reliable and fast as services form. 
## Resources
* XPaths for each element and form are stored on CSV files.
* XPaths for each service are stored at database.
* The information of the services is taken from [servir.csv], the file contents the information from the households which will receive the services. 

[servir.csv]: https://drive.google.com/file/d/1-WM42K0bztgHJFPScD_Acsa2z_aOBp0v/view?usp=sharing
[libreria.py]: libreria.py
[formulario_06.py]: formulario_06.py
[formulario_011.py]: formulario_011.py