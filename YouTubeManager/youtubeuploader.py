from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


def upload_to_youtube(video_path, playlist_name=None):
    # set the path to the Firefox GeckoDriver executable
    webdriver_path = "C:\\Users\\sadee\\Documents\\Coding\\geckodriver-v0.33.0-win64\\geckodriver.exe"
    profile_path = "C:\\Users\\sadee\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\7alihnnu.default-release"
    options = webdriver.FirefoxOptions()
    options.profile = webdriver.FirefoxProfile(profile_path)
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=webdriver_path, options=options)
    driver.implicitly_wait(10)
    driver.get("https://www.youtube.com/upload")
    videoname = video_path[video_path.rfind('\\')+1:-4]
    file_input =  driver.find_element(By.XPATH, '//*[@id="content"]/input')
    file_input.send_keys(video_path)
    time.sleep(10)
    title_field = driver.find_element(By.XPATH, '//*[@id="textbox"]')
    title_field.clear()
    title_field.send_keys(videoname)
    video_url = driver.find_element(By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/ytcp-video-metadata-editor-sidepanel/ytcp-video-info/div/div[2]/div[1]/div[2]/span/a")
    video_url = video_url.get_attribute("href")
    visibility_button = driver.find_element(By.XPATH, '//*[@id="step-badge-3"]')
    visibility_button.click()
    # wait for the video to upload and click the "Publish" button
    start_time = time.time()
    elapsed_time = 0
    while elapsed_time < 1000:
        try:
            processing_started = driver.find_element(By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[1]/ytcp-video-upload-progress/span")
            if 'Processing' in processing_started.text:
                break
        except:
            pass
        time.sleep(60)
        elapsed_time = time.time() - start_time

    publish_button = driver.find_element(By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/div")
    # Scroll the page to make the element visible (if necessary)
    driver.execute_script("arguments[0].scrollIntoView();", publish_button)
    # Click the element using JavaScript
    driver.execute_script("arguments[0].click();", publish_button)
    try:
        close_button_still_processing = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button/div")))
        close_button_still_processing.click()
    except:
        try:
            close_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ytcp-video-share-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button/div")))
            close_button.click()
        except:
            print("Could not locate the close button.")
    time.sleep(10)
    #video_url = driver.current_url #fix
    print(f"{videoname}\nUploaded successfully! URL: {video_url}")
    os.remove(f'{video_path}')
    if playlist_name != None:
        move_video_to_playlist(video_url, playlist_name, driver)
        print(f"Moved {videoname} to {playlist_name} successfully!")
    driver.quit()


def move_video_to_playlist(video_url, playlist_name, driver=None):
    quit_browser = False
    if driver == None:
        # set the path to the Firefox GeckoDriver executable
        webdriver_path = "C:\\Users\\sadee\\Downloads\\geckodriver-v0.33.0-win64\\geckodriver.exe"
        profile_path = "C:\\Users\\sadee\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\7alihnnu.default-release"
        options = webdriver.FirefoxOptions()
        options.profile = webdriver.FirefoxProfile(profile_path)
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=webdriver_path, options=options)
        driver.implicitly_wait(10)
        quit_browser = True
    driver.get("https://studio.youtube.com/")
    content_button = driver.find_element(By.XPATH, "//*[@id='menu-item-1']")
    content_button.click()
    videos_edit = driver.find_elements(By.XPATH, "//*[@id='video-title']")
    for video_edit in videos_edit:
        if video_url[-11:] == video_edit.get_attribute("href")[-16:-5]:
            driver.get(video_edit.get_attribute("href"))
            time.sleep(4)
            playlists_dropdown_button = driver.find_element(By.XPATH, "//*[@id='basics']/div[4]/div[3]/div[1]/ytcp-video-metadata-playlists/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[2]/span")
            playlists_dropdown_button.click()
            almost_playlists = driver.find_elements(By.XPATH, "/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/ytcp-checkbox-group/div/ul/tp-yt-iron-list/div/ytcp-ve")
            playlist_exists = False
            for i, possible_playslist in enumerate(almost_playlists):
                possible_playslist = driver.find_element(By.XPATH, f"/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/ytcp-checkbox-group/div/ul/tp-yt-iron-list/div/ytcp-ve[{i+1}]/li/label/span/span")
                if possible_playslist.get_attribute('innerHTML') == playlist_name:
                    possible_playslist.click()
                    playlist_exists = True
                    break
            if not playlist_exists:
                new_playlist_button = driver.find_element(By.XPATH, "/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/div[2]/div/ytcp-button/div")
                new_playlist_button.click()
                new_playlist_button = driver.find_element(By.XPATH, "/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/div[2]/div/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[1]/ytcp-ve/tp-yt-paper-item-body/div")
                new_playlist_button.click()
                title_field = driver.find_element(By.CSS_SELECTOR, 'html body#html-body ytcp-playlist-creation-dialog ytcp-dialog#dialog.style-scope.ytcp-playlist-creation-dialog tp-yt-paper-dialog#dialog.inline.style-scope.ytcp-dialog div.content.style-scope.ytcp-dialog div.content.style-scope.ytcp-playlist-creation-dialog ytcp-playlist-metadata-editor.style-scope.ytcp-playlist-creation-dialog div.left-col.style-scope.ytcp-playlist-metadata-editor div.input-container.title.style-scope.ytcp-playlist-metadata-editor ytcp-social-suggestions-textbox#title-textarea.style-scope.ytcp-playlist-metadata-editor ytcp-form-input-container#container.fill-height.style-scope.ytcp-social-suggestions-textbox div#outer.style-scope.ytcp-form-input-container div#child-input.style-scope.ytcp-form-input-container div#container-content.style-scope.ytcp-social-suggestions-textbox ytcp-social-suggestion-input#input.fill-height.style-scope.ytcp-social-suggestions-textbox div#textbox.style-scope.ytcp-social-suggestions-textbox')
                title_field.send_keys(playlist_name)
                create_button = driver.find_element(By.XPATH, "/html/body/ytcp-playlist-creation-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/div/ytcp-button[2]/div")
                create_button.click()
                time.sleep(16)
            done_button = driver.find_element(By.XPATH, "/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/div[2]/ytcp-button[2]/div")
            done_button.click()
            save_button = driver.find_element(By.XPATH, "/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[10]/ytcp-video-details-section/ytcp-sticky-header/ytcp-entity-page-header/div/div[2]/ytcp-button[2]/div")
            save_button.click()
            break
    if quit_browser:
        driver.quit()


def playlists_of_channel(channel_url):
    webdriver_path = "C:\\Users\\sadee\\Documents\\Coding\\geckodriver-v0.33.0-win64\\geckodriver.exe"
    profile_path = "C:\\Users\\sadee\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\7alihnnu.default-release"
    options = webdriver.FirefoxOptions()
    options.profile = webdriver.FirefoxProfile(profile_path)
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=webdriver_path, options=options)
    driver.implicitly_wait(10)
    playlists = []
    driver.get(channel_url)
    playlists_button = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab[4]")
    playlists_button.click()
    playlists_buttons = driver.find_elements(By.CSS_SELECTOR, "html body ytd-app div#content.style-scope.ytd-app ytd-page-manager#page-manager.style-scope.ytd-app ytd-browse.style-scope.ytd-page-manager ytd-two-column-browse-results-renderer.style-scope.ytd-browse.grid.grid-5-columns div#primary.style-scope.ytd-two-column-browse-results-renderer ytd-section-list-renderer.style-scope.ytd-two-column-browse-results-renderer div#contents.style-scope.ytd-section-list-renderer ytd-item-section-renderer.style-scope.ytd-section-list-renderer div#contents.style-scope.ytd-item-section-renderer ytd-grid-renderer.style-scope.ytd-item-section-renderer div#items.style-scope.ytd-grid-renderer ytd-grid-playlist-renderer.style-scope.ytd-grid-renderer div#details.style-scope.ytd-grid-playlist-renderer yt-formatted-string#view-more.style-scope.ytd-grid-playlist-renderer a.yt-simple-endpoint.style-scope.yt-formatted-string")
    for playlist in playlists_buttons:
        playlists.append(playlist.get_attribute("href"))
    driver.quit()
    return playlists


if __name__ == "__main__":
    video_folder_path = "C:\\Users\\sadee\\Downloads\\To Do\\Upload To YouTube"
    for video in os.listdir(video_folder_path):
        upload_to_youtube(f"{video_folder_path}\\{video}", "jefkrty  ninfi j sSHHSj")
