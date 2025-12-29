import re
import time
import warnings
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()


class ProfessorScraper:
    def __init__(self, use_selenium: bool = False):
        self.use_selenium = use_selenium
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        self.session.max_redirects = 5
        
    def _init_selenium(self):
        if not SELENIUM_AVAILABLE:
            return False
        if self.driver is None:
            try:
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                return True
            except Exception as e:
                print(f"Selenium 初始化失敗: {str(e)}")
                return False
        return True
    
    def _close_selenium(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def fetch_page(self, url: str) -> Optional[str]:
        try:
            if self.use_selenium and SELENIUM_AVAILABLE:
                if not self._init_selenium() or not self.driver:
                    return None
                try:
                    self.driver.get(url)
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    time.sleep(2)
                    return self.driver.page_source
                except Exception as e:
                    print(f"Selenium 獲取頁面失敗: {str(e)}")
                    return None
            else:
                time.sleep(1)
                response = self.session.get(
                    url, 
                    timeout=20, 
                    verify=False,
                    allow_redirects=True
                )
                response.raise_for_status()
                
                if response.apparent_encoding:
                    response.encoding = response.apparent_encoding
                elif 'charset' in response.headers.get('Content-Type', ''):
                    pass
                else:
                    response.encoding = 'utf-8'
                
                return response.text
        except requests.exceptions.SSLError:
            print(f"SSL 錯誤，嘗試使用 Selenium...")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"連接錯誤: {str(e)}")
            print("嘗試使用 Selenium...")
            return None
        except Exception as e:
            print(f"獲取頁面失敗: {str(e)}")
            return None
    
    def is_valid_name(self, text: str) -> bool:
        if not text or len(text) < 2 or len(text) > 30:
            return False
        
        text = text.strip()
        
        if '@' in text:
            return False
        
        invalid_keywords = [
            'email', 'e-mail', 'contact', 'tel', 'phone', 'fax', 'more', 
            'date', 'time', 'updated', 'posted', 'publish',
            'http', 'www', '.com', '.tw', '.edu',
            'home', 'index', 'about', 'news', 'event', 'course',
            '首頁', '關於', '聯絡', '新聞', '課程', '研究', '下載'
        ]
        text_lower = text.lower()
        for keyword in invalid_keywords:
            if keyword in text_lower:
                return False
        
        date_patterns = [
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
            r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
            r'\d{4}\.\d{1,2}\.\d{1,2}',
            r'\d{4}年\d{1,2}月',
        ]
        for pattern in date_patterns:
            if re.search(pattern, text):
                return False
        
        digit_count = sum(c.isdigit() for c in text)
        if digit_count > len(text) * 0.2:
            return False
        
        chinese_count = sum('\u4e00' <= c <= '\u9fff' for c in text)
        alpha_count = sum(c.isalpha() for c in text)
        
        if chinese_count >= 2:
            if chinese_count <= 4:
                return True
        
        if alpha_count >= 3 and alpha_count <= 25:
            words = text.split()
            if len(words) >= 2 and len(words) <= 4:
                return True
        
        return False
    
    def is_professor_name(self, text: str) -> bool:
        if not self.is_valid_name(text):
            return False
        
        text = text.strip()
        
        chinese_count = sum('\u4e00' <= c <= '\u9fff' for c in text)
        alpha_count = sum(c.isalpha() for c in text)
        
        if chinese_count >= 2 and chinese_count <= 4:
            chinese_surnames = ['王', '李', '張', '劉', '陳', '楊', '黃', '趙', '吳', '周', 
                               '徐', '孫', '馬', '朱', '胡', '林', '郭', '何', '高', '羅',
                               '鄭', '梁', '謝', '宋', '唐', '許', '韓', '馮', '鄧', '曹',
                               '彭', '曾', '肖', '田', '董', '袁', '潘', '於', '蔣', '蔡',
                               '余', '杜', '葉', '程', '蘇', '魏', '呂', '丁', '任', '沈',
                               '方', '石', '姚', '譚', '廖', '鄒', '熊', '金', '陸', '郝',
                               '孔', '白', '崔', '康', '毛', '邱', '秦', '江', '史', '顧',
                               '侯', '邵', '孟', '龍', '萬', '段', '雷', '錢', '湯', '尹',
                               '黎', '易', '常', '武', '喬', '賀', '賴', '龔', '文', '龐']
            if text[0] in chinese_surnames:
                return True
            
            if chinese_count == 2 or chinese_count == 3:
                return True
        
        if alpha_count >= 3 and alpha_count <= 30:
            words = text.split()
            if len(words) >= 1 and len(words) <= 4:
                if all(len(word) >= 2 for word in words):
                    if len(words) == 1:
                        if len(words[0]) >= 3 and words[0][0].isupper():
                            return True
                    else:
                        return True
        
        return False
    
    def extract_email(self, text: str) -> Optional[str]:
        email_patterns = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            r'[a-zA-Z0-9._%+-]+\s*\(at\)\s*[a-zA-Z0-9.-]+\s*\(dot\)\s*[a-zA-Z]{2,}',
            r'[a-zA-Z0-9._%+-]+\s*@\s*[a-zA-Z0-9.-]+\s*\.\s*[a-zA-Z]{2,}'
        ]
        
        for pattern in email_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                email = match.group(0)
                email = email.replace('(at)', '@').replace('(dot)', '.').replace(' ', '')
                return email.lower()
        return None
    
    def extract_department_from_url(self, url: str) -> Optional[str]:
        common_depts = {
            'csie': '資訊工程學系',
            'cs': '資訊科學系',
            'ee': '電機工程學系',
            'me': '機械工程學系',
            'ce': '土木工程學系',
            'chem': '化學系',
            'phys': '物理學系',
            'math': '數學系',
            'bio': '生物學系',
            'econ': '經濟學系',
            'ba': '企業管理學系',
            'law': '法律學系',
        }
        
        url_lower = url.lower()
        for code, dept_name in common_depts.items():
            if f'/{code}/' in url_lower or f'.{code}.' in url_lower:
                return dept_name
        
        return None
    
    def extract_department_from_page(self, soup: BeautifulSoup) -> Optional[str]:
        title = soup.find('title')
        if title:
            title_text = title.get_text()
            dept_keywords = ['系', '所', '學系', '研究所', 'Department', 'Institute']
            if any(keyword in title_text for keyword in dept_keywords):
                for keyword in dept_keywords:
                    if keyword in title_text:
                        parts = title_text.split('-')
                        for part in parts:
                            if keyword in part and len(part.strip()) < 80:
                                return part.strip()
        
        h1_tags = soup.find_all('h1', limit=3)
        for h1 in h1_tags:
            text = h1.get_text(strip=True)
            dept_keywords = ['系', '所', '學系', '研究所', 'Department', 'Institute', '學院']
            if any(keyword in text for keyword in dept_keywords) and len(text) < 80:
                return text
        
        return None
    
    def parse_professor_info(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        professors = []
        
        page_department = self.extract_department_from_page(soup)
        url_department = self.extract_department_from_url(base_url)
        default_department = page_department or url_department
        
        if default_department:
            print(f"頁面科系: {default_department}")
        
        text_content = soup.get_text().lower()
        is_chinese = any(char >= '\u4e00' and char <= '\u9fff' for char in text_content[:1000])
        
        selectors = [
            {'container': 'div.member', 'name': 'h3, h4, .name, strong, .member-name', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department, .division'},
            {'container': 'div.faculty', 'name': 'h2, h3, h4, .name, strong, .faculty-name', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department, .division'},
            {'container': 'div.teacher', 'name': 'h3, h4, .name, strong, .teacher-name', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department, .division'},
            {'container': 'div.profile', 'name': 'h2, h3, h4, .name, strong', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department, .division'},
            {'container': 'li', 'name': 'h3, h4, h5, strong, .name, a', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department, .category'},
            {'container': 'article', 'name': 'h2, h3, .title, strong', 'email': 'a[href^="mailto:"]', 'dept': '.category, .department'},
            {'container': 'div.item', 'name': 'h3, h4, .title, strong, .name', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department'},
            {'container': 'div.card', 'name': 'h3, h4, .title, strong, .name', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department'},
            {'container': '[class*="member"]', 'name': 'h3, h4, strong, .name', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department'},
            {'container': '[class*="faculty"]', 'name': 'h3, h4, strong, .name', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department'},
            {'container': '[class*="teacher"]', 'name': 'h3, h4, strong, .name', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department'},
            {'container': '[class*="professor"]', 'name': 'h3, h4, strong, .name', 'email': 'a[href^="mailto:"]', 'dept': '.dept, .department'},
        ]
        
        for selector_set in selectors:
            containers = soup.select(selector_set['container'])
            
            for container in containers:
                name = None
                email = None
                department = None
                
                name_elem = container.select_one(selector_set['name'])
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    if not self.is_valid_name(name):
                        name = None
                
                all_mailto_links = container.select('a[href^="mailto:"]')
                if all_mailto_links:
                    email = all_mailto_links[0]['href'].replace('mailto:', '').strip().split('?')[0]
                else:
                    email_elem = container.select_one(selector_set['email'])
                    if email_elem:
                        email_text = email_elem.get_text(strip=True)
                        email = self.extract_email(email_text)
                
                if not email:
                    all_text = container.get_text()
                    email = self.extract_email(all_text)
                
                dept_elem = container.select_one(selector_set['dept'])
                if dept_elem:
                    department = dept_elem.get_text(strip=True)
                
                if not department:
                    dept_keywords = ['系', '所', 'Department', 'Institute', '學系', '研究所', '科']
                    for elem in container.find_all(['span', 'p', 'div', 'td', 'li']):
                        text = elem.get_text(strip=True)
                        if any(keyword in text for keyword in dept_keywords) and len(text) < 80:
                            if not email or email not in text:
                                department = text
                                break
                
                if not department:
                    parent = container.find_parent(['div', 'section', 'article'])
                    if parent:
                        for heading in parent.find_all(['h1', 'h2', 'h3']):
                            text = heading.get_text(strip=True)
                            if any(keyword in text for keyword in dept_keywords) and len(text) < 80:
                                department = text
                                break
                
                if name and email and self.is_valid_name(name):
                    final_department = department or default_department or ''
                    
                    if final_department or len(professors) < 50:
                        professors.append({
                            'name': name,
                            'email': email,
                            'department': final_department
                        })
            
            if len(professors) >= 3:
                break
        
        if len(professors) < 3:
            table_rows = soup.select('table tr')
            for row in table_rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    name = None
                    for cell in cells[:3]:
                        potential_name = cell.get_text(strip=True)
                        if self.is_valid_name(potential_name):
                            name = potential_name
                            break
                    
                    if name:
                        email = None
                        department = None
                        
                        for cell in cells:
                            mailto = cell.find('a', href=re.compile(r'mailto:'))
                            if mailto:
                                email = mailto['href'].replace('mailto:', '').strip().split('?')[0]
                            else:
                                cell_text = cell.get_text(strip=True)
                                if not email:
                                    found_email = self.extract_email(cell_text)
                                    if found_email:
                                        email = found_email
                                
                                if not department:
                                    dept_keywords = ['系', '所', 'Department', 'Institute', '學系']
                                    if any(keyword in cell_text for keyword in dept_keywords) and len(cell_text) < 50:
                                        department = cell_text
                        
                        if email:
                            final_department = department or default_department or ''
                            professors.append({
                                'name': name,
                                'email': email,
                                'department': final_department
                            })
        
        if len(professors) < 3:
            all_mailto = soup.find_all('a', href=re.compile(r'mailto:'))
            for link in all_mailto:
                try:
                    email = link['href'].replace('mailto:', '').strip().split('?')[0].split('#')[0]
                    if not email or '@' not in email:
                        continue
                    
                    name = link.get_text(strip=True)
                    
                    if not self.is_valid_name(name):
                        parent = link.find_parent(['div', 'li', 'td', 'article', 'section'])
                        if parent:
                            for elem in parent.find_all(['h3', 'h4', 'h5', 'strong', 'b', 'span'], limit=5):
                                if elem != link and not link in elem.find_all():
                                    potential_name = elem.get_text(strip=True)
                                    if self.is_valid_name(potential_name):
                                        name = potential_name
                                        break
                            
                            if not self.is_valid_name(name):
                                prev_elem = link.find_previous(['h3', 'h4', 'h5', 'strong'])
                                if prev_elem:
                                    potential_name = prev_elem.get_text(strip=True)
                                    if self.is_valid_name(potential_name):
                                        name = potential_name
                    
                    if name and email and self.is_valid_name(name):
                        department = None
                        parent = link.find_parent(['div', 'li', 'td', 'article', 'section'])
                        if parent:
                            dept_keywords = ['系', '所', 'Department', 'Institute', '學系', '研究所']
                            for elem in parent.find_all(['span', 'p', 'div', 'td']):
                                text = elem.get_text(strip=True)
                                if any(keyword in text for keyword in dept_keywords) and len(text) < 50:
                                    department = text
                                    break
                        
                        final_department = department or default_department or ''
                        professors.append({
                            'name': name,
                            'email': email,
                            'department': final_department
                        })
                except Exception as e:
                    continue
        
        return self._deduplicate(professors)
    
    def _deduplicate(self, professors: List[Dict[str, str]]) -> List[Dict[str, str]]:
        seen = set()
        unique_professors = []
        
        for prof in professors:
            if not self.is_valid_name(prof['name']):
                continue
            
            name_clean = re.sub(r'\s+', ' ', prof['name']).strip()
            email_clean = prof['email'].strip().lower()
            
            key = (name_clean.lower(), email_clean)
            if key not in seen:
                seen.add(key)
                prof['name'] = name_clean
                unique_professors.append(prof)
        
        return unique_professors
    
    def scrape_professor_detail(self, detail_url: str, name: str, department: str) -> Optional[Dict[str, str]]:
        try:
            if not detail_url.startswith('http'):
                return None
            
            html = self.fetch_page(detail_url)
            if not html:
                return None
            
            soup = BeautifulSoup(html, 'lxml')
            
            email = None
            all_mailto = soup.find_all('a', href=re.compile(r'mailto:'))
            if all_mailto:
                for link in all_mailto:
                    email_text = link['href'].replace('mailto:', '').strip().split('?')[0].split('#')[0]
                    if email_text and '@' in email_text:
                        email_lower = email_text.lower()
                        if 'contact' not in email_lower and 'info' not in email_lower and 'webmaster' not in email_lower:
                            email = email_text
                            break
            
            if not email:
                all_text = soup.get_text()
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', all_text)
                for em in emails:
                    em_lower = em.lower()
                    if 'contact' not in em_lower and 'info' not in em_lower and 'webmaster' not in em_lower:
                        email = em
                        break
            
            if email and name:
                return {
                    'name': name,
                    'email': email,
                    'department': department
                }
        except Exception as e:
            pass
        
        return None
    
    def is_likely_professor_link(self, link, href: str, link_text: str) -> bool:
        href_lower = href.lower()
        text_lower = link_text.lower()
        
        exclude_keywords = [
            'home', 'index', 'main', 'about', 'contact', 'news', 'event',
            'course', 'curriculum', 'research', 'publication', 'download',
            'login', 'register', 'search', 'menu', 'nav', 'header', 'footer',
            '首頁', '關於', '聯絡', '新聞', '課程', '研究', '登入', '搜尋'
        ]
        
        if any(keyword in text_lower for keyword in exclude_keywords):
            return False
        
        if any(keyword in href_lower for keyword in exclude_keywords):
            return False
        
        if link.find_parent(['nav', 'header', 'footer', '.menu', '.navigation']):
            return False
        
        if '@' in link_text or 'http' in link_text:
            return False
        
        if len(link_text) < 2 or len(link_text) > 30:
            return False
        
        return True
    
    def scrape_with_deep_crawl(self, url: str) -> List[Dict[str, str]]:
        if not SELENIUM_AVAILABLE:
            print("深度爬蟲需要 Selenium，但當前環境不支援")
            return []
        
        print("開始深度爬蟲（點擊連結進入詳細頁面）...")
        
        self.use_selenium = True
        if not self._init_selenium():
            print("無法初始化 Selenium，跳過深度爬蟲")
            return []
        
        try:
            if not self.driver:
                return []
            self.driver.get(url)
            if SELENIUM_AVAILABLE:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            time.sleep(2)
            
            page_department = self.extract_department_from_url(url)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            page_dept = self.extract_department_from_page(soup)
            default_department = page_dept or page_department or ''
            
            professors = []
            professor_links = []
            base_domain = urlparse(url).netloc
            
            all_links = soup.find_all('a', href=True)
            
            for link in all_links:
                href = link.get('href', '')
                if not href:
                    continue
                
                if not href.startswith('http'):
                    href = urljoin(url, href)
                
                if urlparse(href).netloc != base_domain:
                    continue
                
                link_text = link.get_text(strip=True)
                
                if not self.is_professor_name(link_text):
                    continue
                
                if not self.is_likely_professor_link(link, href, link_text):
                    continue
                
                parent_text = ''
                parent = link.find_parent(['div', 'section', 'article', 'li', 'td'])
                if parent:
                    parent_text = parent.get_text()[:200].lower()
                
                if any(keyword in parent_text for keyword in ['menu', 'nav', 'header', 'footer', 'sidebar', '導航', '選單']):
                    continue
                
                href_lower = href.lower()
                link_text_lower = link_text.lower()
                
                has_professor_keyword = any(keyword in href_lower for keyword in [
                    'faculty', 'teacher', 'member', 'people', 'professor', 
                    'staff', 'profile', 'detail', 'info', 'personal'
                ])
                
                has_professor_in_text = any(keyword in link_text_lower for keyword in [
                    '教授', 'professor', '老師', 'teacher', 'faculty'
                ])
                
                is_in_content_area = False
                parent = link.find_parent(['div', 'section', 'article', 'li', 'td'])
                if parent:
                    parent_class = ' '.join(parent.get('class', []))
                    parent_id = parent.get('id', '')
                    content_keywords = ['content', 'main', 'list', 'member', 'faculty', 'people', 'teacher']
                    if any(keyword in parent_class.lower() or keyword in parent_id.lower() for keyword in content_keywords):
                        is_in_content_area = True
                
                if has_professor_keyword or has_professor_in_text or is_in_content_area:
                    if href not in [l['url'] for l in professor_links]:
                        professor_links.append({
                            'name': link_text,
                            'url': href
                        })
            
            if not professor_links:
                print("未找到符合條件的教授連結")
                print("調試資訊：")
                print(f"  - 總連結數: {len(all_links)}")
                test_links = [link.get_text(strip=True) for link in all_links[:10] if link.get_text(strip=True)]
                print(f"  - 前10個連結文字: {test_links}")
                return []
            
            print(f"找到 {len(professor_links)} 個可能的教授連結")
            
            valid_links = []
            for link_info in professor_links[:30]:
                if self.is_professor_name(link_info['name']):
                    valid_links.append(link_info)
                else:
                    print(f"  過濾連結: '{link_info['name']}' (不符合教授姓名格式)")
            
            print(f"驗證後有效連結: {len(valid_links)} 個")
            
            for i, link_info in enumerate(valid_links[:20], 1):
                print(f"  採集 {i}/{min(len(valid_links), 20)}: {link_info['name']}")
                prof_data = self.scrape_professor_detail(
                    link_info['url'],
                    link_info['name'],
                    default_department
                )
                if prof_data and prof_data['email']:
                    if self.is_professor_name(prof_data['name']):
                        professors.append(prof_data)
                        print(f"    ✓ 找到 Email: {prof_data['email']}")
                    else:
                        print(f"    ✗ 姓名驗證失敗")
                else:
                    print(f"    ✗ 未找到 Email")
                time.sleep(0.5)
            
            return professors
            
        finally:
            self._close_selenium()
            self.use_selenium = False
    
    def scrape(self, url: str) -> List[Dict[str, str]]:
        print(f"\n開始採集: {url}")
        
        html = self.fetch_page(url)
        if not html:
            if not self.use_selenium:
                print("嘗試使用 Selenium...")
                self.use_selenium = True
                html = self.fetch_page(url)
                self.use_selenium = False
            
            if not html:
                print("無法獲取頁面內容")
                return []
        
        print(f"頁面內容長度: {len(html)} 字元")
        
        soup = BeautifulSoup(html, 'lxml')
        professors = self.parse_professor_info(soup, url)
        
        print(f"解析結果: {len(professors)} 筆")
        
        if not professors and not self.use_selenium:
            print("嘗試使用 Selenium 動態渲染...")
            self.use_selenium = True
            html = self.fetch_page(url)
            if html:
                soup = BeautifulSoup(html, 'lxml')
                professors = self.parse_professor_info(soup, url)
                print(f"Selenium 解析結果: {len(professors)} 筆")
            self.use_selenium = False
        
        if not professors or len(professors) < 3:
            print("\n列表頁面未找到足夠資料，嘗試深度爬蟲...")
            deep_professors = self.scrape_with_deep_crawl(url)
            if deep_professors:
                professors = deep_professors
                print(f"深度爬蟲成功採集 {len(professors)} 筆")
        
        if professors:
            print(f"\n✓ 成功採集 {len(professors)} 筆教授資料")
            print("=" * 70)
            for i, prof in enumerate(professors[:10], 1):
                print(f"{i}. 姓名: {prof['name']:<20} | Email: {prof['email']:<30}")
                print(f"   科系: {prof['department'] or '(未取得)'}")
                if i < len(professors[:10]):
                    print("-" * 70)
        else:
            print("✗ 未找到任何教授資料")
            all_mailto = soup.find_all('a', href=re.compile(r'mailto:'))
            print(f"頁面中共找到 {len(all_mailto)} 個 mailto 連結")
            if all_mailto:
                print("  範例連結:")
                for link in all_mailto[:3]:
                    print(f"    - {link.get('href')} | 文字: '{link.get_text(strip=True)}'")
            
            all_headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])
            print(f"頁面中共找到 {len(all_headings)} 個標題元素")
        
        self._close_selenium()
        return professors

