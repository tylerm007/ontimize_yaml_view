import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'YamlFiles-new',
  templateUrl: './YamlFiles-new.component.html',
  styleUrls: ['./YamlFiles-new.component.scss']
})
export class YamlFilesNewComponent {
  @ViewChild('YamlFilesForm') form: OFormComponent;

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
      const {files} = event.target as HTMLInputElement;
      let declare_logic;
      let app_model;
      let project_name = "ApiLogicServer";
      if (files && output) {
        
        for (let i = 0; i < files.length; i++) {
          if (i == 0) {
            URL.createObjectURL(files[i]).split("/").forEach((path) => {
              project_name = "Project_"+ path;
              console.log(project_name);
              return;
            });
          }
          if (files[i].type == "text/x-python-script" && files[i].name == "declare_logic.py") {
            //console.log(URL.createObjectURL(files[i]));
            //console.log(files[i].name, files[i].webkitRelativePath);
            //const item = document.createElement("li");
            //item.innerHTML = files[i].webkitRelativePath;
            //output.appendChild(item);
            declare_logic = await files[i].text();
            
          }
          if (files[i].type == "application/x-yaml" && files[i].name == "app_model.yaml") {
            //console.log(URL.createObjectURL(files[i]));
            //console.log(files[i].name, files[i].type, files[i].webkitRelativePath);
            //const item = document.createElement("li");
            //item.innerHTML = files[i].webkitRelativePath;
            //output.appendChild(item);
            app_model = await files[i].text();
          }
        }
        if (app_model && declare_logic) {
          console.log(declare_logic, app_model);
          const encodedAppModel = btoa(app_model);
          const encodedLogicModel = btoa(declare_logic);
          this.form.setFieldValues({ "name": project_name, "content": encodedAppModel, "rule_content": encodedLogicModel });
            const field = this.form.getFieldValue('content');
            if (field) {
              field.visible = false;
            }
            const field2 = this.form.getFieldValue('rule_content');
            if (field2) {
              field2.visible = false;
            }
        } else {
          alert("Please select an ApiLogicServer project folder");
        }
      }
    }, false);
  }
}