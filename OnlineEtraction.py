import urllib2
import re
import csv

shixiseng = "http://www.shixiseng.com"

def URLcontent(URL):
    """
    give the content from given URL or print error
    input : URL string
    output : string(html form)
    """
    try:
        content = urllib2.urlopen(URL).read()
    except OSError:
        print "error occured"
    return content

def getSearchURL(URL):
    """this return a list of match object in which contains raw html lines containing jobs information
        input : URL sting
        output : list of match object
    """
    content = URLcontent(URL)
    string = "<a\ data-sa=\"open\" data-smod=\"list_content\" data-starget=\"(.*?)\" data-sinfo=\"{'type':'intern'}\" href=\"(.*?)\" title=\"(.*?)\" target=\"_blank\">"
    found = re.finditer(string,content)
    return found

def extractJobNameInformation(jobURLstring):
    """
    give out job name
    input : string
    output : string
    """
    matchstring = "<span class=\"job_name\" title=\"(.*?)\">(.*?)</span>"
    found = re.search(matchstring,jobURLstring)
    if found:
        jobName = found.group(1)
    else :
        return "N/A"
    return jobName

def extractCompanyName(jobURLstring):
    """
    give our company name
    input : string
    output : string
    """
    matchstring = "<p><a href=\"/company/detail/com(.*?)\">(.*?)</a></p>"
    found = re.search(matchstring,jobURLstring)
    if found:
        companyName = found.group(2)
    else:
        return "N/A"
    return companyName

def extractCityName(jobURLstring):
    """
    give our city name
    input : string
    output : string
    """
    matchstring = "<span class=\"city\" title=\"(.*?) \">(.*?)</span>"
    found = re.search(matchstring,jobURLstring)
    if found:
        cityName = found.group(1)
    else:
        return "N/A"
    return cityName

def extractJobDescription(jobURLString):
    """
    extract job description

    input :  string
    ouput : string
    """
    description_flag = "<div class=\"dec_content\">"
    start_point = jobURLString.find(description_flag)
    end_flag = "</div>"
    end_point = jobURLString.find(end_flag,start_point)
    current_point = start_point
    p_flag = "<p>"
    pp_flag = "</p>"
    description = ""
    while current_point <  end_point:
        p_start = jobURLString.find(p_flag,current_point)
        p_end = jobURLString.find(pp_flag,current_point)
        one_line = jobURLString[p_start:p_end]
        description += "\n" + extractText(one_line)
        current_point = p_end + 4
    return description


def extractText(HTMLstring):
    """
    This method clear the non sense sign, syntax to give clean text
    input : string
    output : string
    """

    output = HTMLstring[3:]
    output = output.replace("&nbsp;"," ")
    output = output.replace("<br>", "")
    output = output.replace("<span></span>","")
    return output

def main():
    """
    This function integrate all the methods above to finish the functionality
    """
    found = getSearchURL("https://www.shixiseng.com/interns?k=%E7%B2%BE%E7%AE%97&p=1")
    list = ["Company","Title","City","Job Description","URL"]
    with open('results.csv', 'wb') as f:
        f.write(u'\ufeff'.encode('utf8'))
        w = csv.writer(f)
        w.writerow(list)
        for m in found:
            jobURL = shixiseng+m.group(2)
            content = URLcontent(jobURL)
            jobName = extractJobNameInformation(content)
            jobCompany = extractCompanyName(content)
            jobCity = extractCityName(content)
            jobDescription = extractJobDescription(content)
            print "name: " + jobName
            print "company: " + jobCompany
            print "city: " + jobCity
            print "job description: "+jobDescription
            print "\n"
            this = [jobCompany,jobName,jobCity,jobDescription,jobURL]
            w.writerow(this)


if __name__ == "__main__":
    main()