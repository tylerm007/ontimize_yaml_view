import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {APPLICATION_MODULE_DECLARATIONS, ApplicationRoutingModule} from  './Application-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ApplicationRoutingModule
  ],
  declarations: APPLICATION_MODULE_DECLARATIONS,
  exports: APPLICATION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ApplicationModule { }