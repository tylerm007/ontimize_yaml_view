import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {MENUGROUP_MODULE_DECLARATIONS, MenuGroupRoutingModule} from  './MenuGroup-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    MenuGroupRoutingModule
  ],
  declarations: MENUGROUP_MODULE_DECLARATIONS,
  exports: MENUGROUP_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class MenuGroupModule { }