import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent, SnackBarService } from 'ontimize-web-ngx';
//import {MAT_SNACK_BAR_DATA} from '@angular/material/snack-bar';
@Component({
  selector: 'YamlFiles-new',
  templateUrl: './YamlFiles-new.component.html',
  styleUrls: ['./YamlFiles-new.component.scss']
})

export class YamlFilesNewComponent {
  @ViewChild('YamlFilesForm') form: OFormComponent;
  protected snackBarService: SnackBarService
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
  onInsertMode() {
    const default_values = { "name": "app_model.yaml" };
    this.form.setFieldValues(default_values);
  }

  ngAfterViewInit() {
    document.getElementById("folder")?.addEventListener("change", async (event: Event) => {
      const output = document.querySelector("ul");
      const { files } = event.target as HTMLInputElement;
      const fullPath = (event.target as HTMLInputElement).files[0].webkitRelativePath;
      const filePaths = Array.from(files).map(file => file.webkitRelativePath || file.name);

      console.log(filePaths);
      //console.log(fullPath);
      let declare_logic;
      let declare_security;
      let app_model = [];
      let app_model_raw = [];
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
            declare_logic = await files[i].text();

          }
          // this may change with discovery of other logic files in the future
          if (files[i].type == "text/x-python-script" && files[i].name == "declare_security.py") {
            declare_security = await files[i].text();

          }
          // Send one or more files to the server
          if (files[i].type == "application/x-yaml" && files[i].name == "app_model.yaml") {
            let app_yaml = await files[i].text();
            let model = btoa(app_yaml)
            app_model_raw.push(app_yaml);
            app_model.push(model);
            let field = this.form.getFieldValue('content');
            field.setValue(app_yaml);
          }
        }
        if (app_model) {
          for (let i in app_model) {
            console.log(declare_logic, app_model);
            let encodedAppModel = app_model[i] //btoa(app_model);
            let encodedLogicModel = declare_logic ? btoa(declare_logic) : null;
            let encodedSecurityModel = declare_security ? btoa(declare_security) : null;
            let app_name = "app" //TODO
            this.form.setFieldValues({ "name": project_name + (i + 1), "content": encodedAppModel, "rule_content": encodedLogicModel, "role_content": encodedSecurityModel,"app_name": app_name });
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
            this.snackBarService.open('Uploading files...');
          }
        } else {
          alert("Please select a root ApiLogicServer project folder");
        }
      }
    }, false);
  }
}