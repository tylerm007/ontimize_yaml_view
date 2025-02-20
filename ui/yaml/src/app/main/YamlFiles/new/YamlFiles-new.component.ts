import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent, SnackBarService,  OSnackBarConfig} from 'ontimize-web-ngx';
//import {MAT_SNACK_BAR_DATA} from '@angular/material/snack-bar';
@Component({
  selector: 'YamlFiles-new',
  templateUrl: './YamlFiles-new.component.html',
  styleUrls: ['./YamlFiles-new.component.scss']
})

export class YamlFilesNewComponent {
  @ViewChild('YamlFilesForm') form: OFormComponent;
  public snackBarService: SnackBarService;
  public snackBarConfig: OSnackBarConfig;
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
    this.snackBarService = this.injector.get(SnackBarService);
  }
  onInsertMode() {
    const default_values = { "name": "app_model.yaml" };
    this.form.setFieldValues(default_values);
    this.form.setFieldValues({"app_name": "app"});
  }

  ngAfterViewInit() {
    document.getElementById("folder")?.addEventListener("change", async (event: Event) => {
      const output = document.querySelector("ul");
      const { files } = event.target as HTMLInputElement;
      const fullPath = (event.target as HTMLInputElement).files[0].webkitRelativePath;
      const filePaths = Array.from(files).map(file => file.webkitRelativePath || file.name);

      //console.log(filePaths[0]);
      //console.log(fullPath);
      let declare_logic;
      let declare_security;
      let wg_all_rules;
      let local_storage = [];
      let en_json = [];
      let app_model = [];
      let app_model_raw = [];
      let app_names = [];
      let project_name = "ApiLogicServer";
      if (files && output) {

        for (let i = 0; i < files.length; i++) {
          if (i == 0) {
            URL.createObjectURL(files[i]).split("/").forEach((path) => {
              project_name = "Project_";
              console.log(project_name);
              return;
            });
          }
          if (files[i].type == "text/x-python-script" && files[i].name == "declare_logic.py") {
                let dir = URL.createObjectURL(files[i]).split("/")[0]; //Root folder
                if  (dir == "logic" )  {
                  console.log(dir, "declare_logic.py");
                  declare_logic = await files[i].text();
                }
          }
          // this may change with discovery of other logic files in the future
          if (files[i].type == "text/x-python-script" && files[i].name == "declare_security.py") {
            declare_security = await files[i].text();
          }
          if (files[i].type == "text/x-python-script" && files[i].name  == "active_rules_export.py") {
              console.log("active_rules_export.py");
              wg_all_rules = await files[i].text();
          }

          // Send one or more files to the server
          if (files[i].type == "application/x-yaml" && files[i].name == "app_model.yaml") {
            let app_yaml = await files[i].text();
            let model = btoa(app_yaml)
            app_model_raw.push(app_yaml);
            app_model.push(model);
            app_names.push(files[i].webkitRelativePath.split("/")[2]);
            let field = this.form.getFieldValue('content');
            if (field) {
              field.setValue(app_yaml);
            }
            console.log("app_names", app_names);
          }
          if (files[i].type == "application/json" && files[i].name.startsWith("com.ontimize.web.ngx")) {
            let ls = await files[i].text();
            local_storage.push(ls);
          }
          if (files[i].type == "application/json" && files[i].name == "en.json") {
            let en = await files[i].text();
            en_json.push(en);
          }
        }
        if (app_model) {
          // For each app_model.yaml project - create a new entry
          for (let i in app_model) {
            console.log(declare_logic, app_model, declare_logic, wg_all_rules);
            if (wg_all_rules) {
              console.log("wg_all_rules");
              declare_logic = declare_logic ? declare_logic += wg_all_rules: wg_all_rules;
            }
            let encodedAppModel = app_model[i] //btoa(app_model);
            let encodedLogicModel = declare_logic ? btoa(declare_logic) : null;
            let encodedSecurityModel = declare_security ? btoa(declare_security) : null;
            let encodedLocalStorage = local_storage.length > 0 ? btoa(local_storage[i]) : null;
            if (local_storage.length == 0) {
              const localStorageElement = document.getElementById('local_storage');
              if (localStorageElement) {
                let ls = localStorageElement.textContent || '';
                encodedLocalStorage = btoa(ls);
              }
            }
            let file_path = this.form.getFieldValue('file_path');
            let app_name = app_names[i]
            this.form.setFieldValues({ 
                "name": project_name + app_name + "_" + (i + 1), 
                "app_name": app_name,
                "download_flag": false,
                "content": encodedAppModel, 
                "rule_content": encodedLogicModel, 
                "role_content": encodedSecurityModel,
                "local_storage": encodedLocalStorage,
                "en_json":en_json[i], 
                "file_path": file_path || filePaths[i].split("/").pop()
              });
            let field = this.form.getFieldValue('content');
            if (field && app_model_raw[0]) {
              console.log("app_model_raw[0]");
              //field.setValue(app_model_raw[0]);
            }
            let field2 = this.form.getFieldValue('rule_content');
            if (field2 && declare_logic) {
              console.log("declare_logic");
              //field2.setValue(declare_logic);
            }
            let field3 = this.form.getFieldValue('role_content');
            if (field3 && declare_security) {
              console.log("declare_security");
              //field3.setValue(declare_security);
            }
            let field4 = this.form.getFieldValue('local_storage');
            if (field4 && local_storage.length > 0 && local_storage[i]) {
              console.log("local_storage", local_storage[i]);
              //field3.setValue(local_storage);
            }
            const configuration: OSnackBarConfig = {
              action: 'Ok',
              milliseconds: 3000,
              icon: 'check_circle',
              iconPosition: 'left'
            }
            this.snackBarService.open('Uploading selected files...', configuration);
          }
        } else {
          alert("Please select a root ApiLogicServer project folder");
        }
      }
    }, false);
  }
}