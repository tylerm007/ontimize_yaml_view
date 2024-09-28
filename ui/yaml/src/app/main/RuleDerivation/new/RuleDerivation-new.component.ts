import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'RuleDerivation-new',
  templateUrl: './RuleDerivation-new.component.html',
  styleUrls: ['./RuleDerivation-new.component.scss']
})
export class RuleDerivationNewComponent {
  @ViewChild("RuleDerivationForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}