class Course:

    def __init__(self, uni_domain: str, **course_info):
        self.__crn = "CRN was not specified"
        self.__url = f"https://{uni_domain}.edu/bprod/bwckschd.p_disp_detail_sched?" # Ellucian web portal link format
        # Formats URL
        for query, value in course_info.items():
            self.__url += f"{query}={value}&"
            
            if query.upper().__contains__("CRN"):
                self.__crn = value

    # Getter for url
    @property
    def url(self):
        return self.__url
    
    # Getter for crn
    @property
    def crn(self):
        return self.__crn
    
    # Setter
    @url.setter
    def url(self, value):
        new_url, course_info = value[0], value[1]

        for query, value in course_info.items():
            new_url += f"{query}={value}&"
        self.__url = new_url