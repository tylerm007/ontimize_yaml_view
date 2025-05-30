import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PAGEPROPERTY_MODULE_DECLARATIONS, PagePropertyRoutingModule} from  './PageProperty-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PagePropertyRoutingModule
  ],
  declarations: PAGEPROPERTY_MODULE_DECLARATIONS,
  exports: PAGEPROPERTY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PagePropertyModule { }