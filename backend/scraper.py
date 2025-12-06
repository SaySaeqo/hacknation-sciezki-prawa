import requests
from bs4 import BeautifulSoup

BASE_URL = "https://legislacja.rcl.gov.pl"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def get_projects_list():
    url = f"{BASE_URL}/lista?typeId=2"
    response = requests.get(url, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table')
    if not table:
        return []
    
    rows = table.find_all('tr')[1:]
    
    projects = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 5:
            title_link = cols[0].find('a')
            title = title_link.text.strip() if title_link else cols[0].text.strip()
            link = title_link['href'] if title_link else None
            project_id = link.split('/')[-1] if link else None
            applicant = cols[1].text.strip()
            number = cols[2].text.strip()
            create_date = cols[3].text.strip()
            progress = cols[4].text.strip()
            
            projects.append({
                "id": project_id,
                "title": title,
                "applicant": applicant,
                "number": number,
                "create_date": create_date,
                "progress": progress
            })
    
    return projects

def get_project_details(project_id):
    url = f"{BASE_URL}/projekt/{project_id}"
    response = requests.get(url, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    details = {}
    
    
    applicant_text = soup.find(text=lambda t: t and 'Wnioskodawca:' in t)
    if applicant_text:
        applicant = applicant_text.find_next('a').text.strip() if applicant_text.find_next('a') else None
        details['wnioskodawca'] = applicant
    
   
    create_date_text = soup.find(text=lambda t: t and 'Data utworzenia:' in t)
    if create_date_text:
        create_date = create_date_text.find_next('a').text.strip() if create_date_text.find_next('a') else None
        details['data_utworzenia'] = create_date
    
 
    dept_text = soup.find(text=lambda t: t and 'Działy:' in t)
    if dept_text:
        next_sib = dept_text.parent.find_next_sibling()
        if next_sib:
            depts = [a.text.strip() for a in next_sib.find_all('a')]
            details['dzialy'] = depts
    
    
    keywords_text = soup.find(text=lambda t: t and 'Hasła:' in t)
    if keywords_text:
        next_sib = keywords_text.parent.find_next_sibling()
        if next_sib:
            keywords = [a.text.strip() for a in next_sib.find_all('a')]
            details['hasla'] = keywords
    
   
    kadencja_text = soup.find(text=lambda t: t and 'Kadencja:' in t)
    if kadencja_text:
        next_sib = kadencja_text.parent.find_next_sibling()
        if next_sib:
            kadencja = next_sib.get_text().strip()
            details['kadencja'] = kadencja
    
    
    okres_text = soup.find(text=lambda t: t and 'Okres kadencji:' in t)
    if okres_text:
        next_sib = okres_text.parent.find_next_sibling()
        if next_sib:
            okres = next_sib.get_text().strip()
            details['okres_kadencji'] = okres
    
    
    details['status_projektu'] = 'otwarty'
    
  
    numer_text = soup.find(text=lambda t: t and 'Numer z wykazu:' in t)
    if numer_text:
        next_sib = numer_text.parent.find_next_sibling()
        if next_sib:
            numer = next_sib.get_text().strip()
            details['numer_z_wykazu'] = numer
    
    
    wykaz_text = soup.find(text=lambda t: t and 'Wykaz prac legislacyjnych:' in t)
    if wykaz_text:
        next_sib = wykaz_text.parent.find_next_sibling()
        if next_sib:
            wykaz = next_sib.get_text().strip()
            details['wykaz_prac_legislacyjnych'] = wykaz
    
   
    zwolniony_text = soup.find(text=lambda t: t and 'Projekt zwolniony' in t)
    if zwolniony_text:
        details['projekt_zwolniony'] = zwolniony_text.strip()
    
    stages = []
    katalog_links = soup.find_all('a', href=lambda href: href and '/katalog/' in href)
    for link in katalog_links:
        stage_name = link.text.strip()
        href = link['href']
        katalog_id = href.split('/')[-1].split('#')[0]
        parent = link.parent
        full_text = parent.get_text()
        date = None
        if 'Data ostatniej modyfikacji:' in full_text:
            date = full_text.split('Data ostatniej modyfikacji:')[1].strip().split()[0]
        
        stages.append({
            "name": stage_name,
            "katalog_id": katalog_id,
            "date": date
        })
    
    return {
        "details": details,
        "stages": stages
    }

def get_stage_details(project_id, katalog_id):
    try:
        url = f"{BASE_URL}/projekt/{project_id}/katalog/{katalog_id}"
        response = requests.get(url, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        documents = []
        doc_links = soup.find_all('a', href=lambda href: href and '/docs/' in href)
        for link in doc_links:
            doc_type = link.text.strip()
            doc_link = link['href']
            if doc_link.startswith('/'):
                doc_link = BASE_URL + doc_link
            parent = link.parent
            full_text = parent.get_text()
            author = None
            date = None
            if 'Autor dokumentu:' in full_text:
                author_part = full_text.split('Autor dokumentu:')[1].split(',')[0].strip()
                author = author_part
            if 'Data utworzenia:' in full_text:
                date_part = full_text.split('Data utworzenia:')[1].strip().split()[0]
                date = date_part
            
            documents.append({
                "type": doc_type,
                "link": doc_link,
                "author": author,
                "date": date
            })
        
        sections = {}
        if len(documents) >= 3:
            sections["Projekt"] = documents[:3]
            sections["Pisma kierujące projekt do opiniowania"] = documents[3:]
        else:
            sections["Documents"] = documents
        
        return sections
    except Exception as e:
        return {"error": str(e)}