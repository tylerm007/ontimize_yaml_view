import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {APPLICATIONENTITY_MODULE_DECLARATIONS, ApplicationEntityRoutingModule} from  './ApplicationEntity-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ApplicationEntityRoutingModule
  ],
  declarations: APPLICATIONENTITY_MODULE_DECLARATIONS,
  exports: APPLICATIONENTITY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ApplicationEntityModule { }