import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {RULEEVENT_MODULE_DECLARATIONS, RuleEventRoutingModule} from  './RuleEvent-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    RuleEventRoutingModule
  ],
  declarations: RULEEVENT_MODULE_DECLARATIONS,
  exports: RULEEVENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class RuleEventModule { }