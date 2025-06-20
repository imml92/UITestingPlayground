import pytest
from models.login_page import LoginPage
from playwright.sync_api import TimeoutError, BrowserContext, Page, expect, Browser, Playwright

@pytest.fixture(autouse=True)
def page(playwright: Playwright):
    browser = playwright.chromium.launch(args=['--start-maximized'], headless=False)
    page = browser.new_page(no_viewport=True)
    print("\n[ Fixture ]: Opening page...\n")
    page.goto("http://uitestingplayground.com/")

    yield page

    page.close()
    print("\n[ Fixture ]: page closed")

# @pytest.fixture(scope="session")
# def browser_type_launch_args():
#     return {
#         "headless": False,
#         "slow_mo": 500,
#     }

def test_dinamic_id(page: Page):
    page.get_by_role("link",name="Dynamic ID").click()

    btn = page.get_by_role("button", name="Button with Dynamic ID")
    expect(btn).to_be_visible()

    btn.click()

def test_class(page: Page):
    page.get_by_role("link",name="Class Attribute").click()

    btn = page.locator("button.btn-primary")
    # With XPath
    # btn = page.locator("//button["contains(@class, 'btn-primary']")
    expect(btn).to_be_visible()

    btn.click()

def test_hidden_layer(page: Page):
    page.get_by_role("link",name="Hidden Layers").click()

    btn = page.locator("button.btn-success")
    btn.click()

    # We know that it will fail
    with pytest.raises(TimeoutError):
        btn.click(timeout=2000)

def test_load_delays(page: Page):
    page.get_by_role("link",name="Load Delay").click()

    btn = page.get_by_role("button", name="Button Appearing After Delay")
    btn.wait_for(timeout=10_000)
    expect(btn).to_be_visible()

def test_ajax_data(page: Page):
    page.get_by_role("link",name="AJAX Data").click()

    btn = page.get_by_role("button", name="Button Triggering AJAX Request")
    expect(btn).to_be_visible()
    btn.click()

    paragraph = page.locator("p.bg-success")
    paragraph.wait_for()
    expect(paragraph).to_be_visible()

def test_click(page: Page):
    page.get_by_role("link",name="Click").click()

    btn = page.get_by_role("button", name="Button That Ignores DOM Click Event")
    expect(btn).to_be_visible()
    btn.click()

    expect(btn).to_have_class("btn btn-success")

def test_input_text(page: Page):
    page.get_by_role("link",name="Text Input").click()

    query = "great stuff"
    input = page.get_by_label("Set New Button Name")
    expect(input).to_be_visible()
    input.fill(query)

    btn = page.locator("button.btn-primary")
    btn.click()
    expect(btn).to_have_text(query)

def test_scrollbars(page: Page):
    page.get_by_role("link",name="Scrollbars").click()

    btn = page.get_by_role("button", name="Hiding Button")
    btn.scroll_into_view_if_needed()

    expect(btn).to_be_visible()

def test_dynamic_table(page: Page):
    page.get_by_role("link",name="Dynamic Table").click()

    label = page.locator("p.bg-warning").inner_text()
    percentage = label.split()[-1]
    print(f"[ Test ]: Label % value: {percentage}")

    # Obtenemos la columna del porcentaje de CPU
    column_headers = page.get_by_role("columnheader")
    cpu_column = None

    for index in range(column_headers.count()):
        column_header = column_headers.nth(index)

        if column_header.inner_text() == "CPU":
            cpu_column = index
            break

    assert cpu_column != None

    # Obtenemos la fila de Chrome
    rowgroup = page.get_by_role("rowgroup").last
    chrome_row = rowgroup.get_by_role("row").filter(
        has_text="Chrome"
    )

    # Obtenemos el valor de la celda de CPU para Chrome
    chrome_cpu = chrome_row.get_by_role("cell").nth(cpu_column)
    print(f"[ Test ]: Table value: {chrome_cpu.inner_text()}")

    expect(chrome_cpu).to_have_text(percentage)

def test_verify_text(page: Page):
    page.get_by_role("link",name="Verify Text").click()

    text = page.locator("div.bg-primary").get_by_text("Welcome")

    expect(text).to_have_text("Welcome UserName!")

def test_progress_bar(page: Page):
    page.get_by_role("link",name="Progress Bar").click()

    start = page.get_by_role("button", name="Start")
    stop = page.get_by_role("button", name="Stop")
    progressbar = page.get_by_role("progressbar")

    start.click()

    while True:
        valuenow = int(progressbar.get_attribute("aria-valuenow"))
        if valuenow >= 75:
            stop.click()
            print(f"[ Test ]: stopped at {valuenow}%")
            break

    assert valuenow >= 75

def test_visibility(page: Page):
    page.get_by_role("link",name="Visibility").click()

    hide_btn = page.get_by_role("button", name="Hide")
    removed_btn = page.get_by_role("button", name="Removed")
    zero_width_btn = page.get_by_role("button", name="Zero Width")
    overlapped_btn = page.get_by_role("button", name="Overlapped")
    opacity_btn = page.get_by_role("button", name="Opacity 0")
    hidden_btn = page.get_by_role("button", name="Visibility Hidden")
    display_none_btn = page.get_by_role("button", name="Display None")
    offscreen_btn = page.get_by_role("button", name="Offscreen")

    hide_btn.click()

    expect(removed_btn).to_be_hidden()
    expect(zero_width_btn).to_have_css("width", "0px")
    with pytest.raises(TimeoutError):
        overlapped_btn.click(timeout=2000)
    expect(opacity_btn).to_have_css("opacity", "0")
    expect(hidden_btn).to_be_hidden()
    expect(display_none_btn).to_be_hidden()
    expect(offscreen_btn).not_to_be_in_viewport()

def test_succesful_login(page: Page):
    username = "rina"

    loginPage = LoginPage(page)
    loginPage.login(
        username, "pwd"
    )

    expect(loginPage.loginstatus).to_have_text(f"Welcome, {username}!")

def test_failed_login(page: Page):
    username = "rina"

    loginPage = LoginPage(page)
    loginPage.login(
        username, "pwdxxx"
    )

    expect(loginPage.loginstatus).to_have_text("Invalid username/password")

def test_mouse_over(page: Page):
    page.get_by_role("link",name="Mouse Over").click()

    link = page.get_by_title("Click me")
    link.hover()

    # Some attributes may change
    active_link = page.get_by_title("Active Link")
    active_link.dblclick()

    counter = page.locator("span#clickCount")

    expect(counter).to_have_text("2")

def test_non_breaking_space(page: Page):
    page.get_by_role("link",name="Non-Breaking Space").click()

    btn = page.locator("//button[text()='My\u00a0Button']")
    # If you do like this, it wont fail
    # btn = page.get_by_role("button", name="My Button")
    btn.click(timeout=2000)

    expect(btn).to_be_visible()

def test_overlapped_element(page: Page):
    page.get_by_role("link",name="Overlapped Element").click()

    overlapped = page.get_by_placeholder("Name")

    print("Text before scroll down:", overlapped.input_value())
    expect(overlapped).to_be_visible()

    # It doesnt work because we are seeing a fraction of the element
    # overlapped.scroll_into_view_if_needed()
    div = overlapped.locator("..")
    div.hover()
    
    page.mouse.wheel(0, 200)
    # We have to wait for the element to be displayed
    overlapped.wait_for()

    overlapped.fill("rina")

    print("Text after scroll down:", overlapped.input_value())

    expect(overlapped).to_have_value("rina")
