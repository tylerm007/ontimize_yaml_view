import { Injector, Component, ViewChild, ViewEncapsulation } from '@angular/core';
import { MatRadioChange } from '@angular/material/radio';
import { MatSlideToggle, MatSlideToggleChange } from '@angular/material/slide-toggle';
import { OntimizeService, LocalStorageService, SessionInfo, AppConfig, AppearanceService, OTranslateService, Util, OFormComponent, SnackBarService, OSnackBarConfig } from 'ontimize-web-ngx';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.app-settings]': 'true'
  }
})
export class SettingsComponent {
  protected service: any;
  public availableLangs: string[] = [];
  public currentLang: string;
  public darkDefaultMode = false;
  public localStorage = []
  public snackBarService: SnackBarService;
  public snackBarConfig: OSnackBarConfig;
  @ViewChild('MyForm') form: OFormComponent;

  @ViewChild('toggleDark')
  private toggleDark: MatSlideToggle;

  constructor(
    private _appConfig: AppConfig,
    private _translateService: OTranslateService,
    private appearanceService: AppearanceService,
    protected injector: Injector
  ) {
    this.service = this.injector.get(OntimizeService);
    this.darkDefaultMode = this.appearanceService.isDarkMode();
    this.availableLangs = this._appConfig.getConfiguration().applicationLocales;
    this.currentLang = this._translateService.getCurrentLang();
    this.snackBarService = this.injector.get(SnackBarService);
  }

  changeLang(e: MatRadioChange): void {
    if (this._translateService && this._translateService.getCurrentLang() !== e.value) {
      this._translateService.use(e.value);
    }
  }


  changeDarkMode(e: MatSlideToggleChange): void {
    this.appearanceService.setDarkMode(e.checked);
  }
  public getDownloaded() {
    let downloaded = ''
    if (this.localStorage.length > 0) {

      const configuration: OSnackBarConfig = {
        action: 'Ok',
        milliseconds: 1000,
        icon: 'check_circle',
        iconPosition: 'left'
      }
      //this.snackBarService.open("Please wait, Downloading Local Storage..", configuration);
      const downloaded = JSON.stringify(this.localStorage);
      console.log("getDownloaded " + downloaded);
    }
    //this.form.setFieldValue("downloaded", downloaded);
    return downloaded;
  }
  public getLocalStorageService() {
    if (this.localStorage.length > 0) {
      console.log("LocalStorage already processed");
      return this.localStorage;
    }
    const configuration: OSnackBarConfig = {
      action: 'Ok',
      milliseconds: 2000,
      icon: 'check_circle',
      iconPosition: 'left'
    }
    this.snackBarService.open("Please wait, Processing Local Storage..", configuration);
    let componentData = this.getSessionUserComponentsData();
    for (let key in componentData) {
      const decoded = atob((componentData[key]));
      console.log("Component: ", key, decoded);
      let j = JSON.parse(decoded) || {};
      if (j.hasOwnProperty("oColumns-display")) { 
        this.localStorage.push({ "key": key, "oColumns-display": j["oColumns-display"]});
      }
    }
    //console.log("LocalStorage: ", this.localStorage);
    const element = document.getElementById('downloaded');
    if (element) {
      let { uuid } = this._appConfig.getConfiguration();
      element.innerText = JSON.stringify(this.localStorage);
      const blob = new Blob([JSON.stringify(this.localStorage, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = uuid + '.json';
      a.click();
      URL.revokeObjectURL(url);
    }
    return this.localStorage;
  }
  public getSessionUserComponentsData(): object {
    //let storedComponentsByUser = {};
    const appData = this.getStoredData();
    const session: SessionInfo = appData[LocalStorageService.SESSION_STORAGE_KEY] || {};
    const users = appData[LocalStorageService.USERS_STORAGE_KEY] || {};
    return (users[session.user] || {})[LocalStorageService.COMPONENTS_STORAGE_KEY] || {};
  }
  public getStoredData(): object {
    let appData = {};
    let { uuid } = this._appConfig.getConfiguration();
    const appStoredData = localStorage.getItem(uuid);
    if (appStoredData) {
      try {
        appData = JSON.parse(appStoredData);
      } catch (e) {
        appData = {};
      }
    }
    return appData;
  }
}
