import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {GRANTROLE_MODULE_DECLARATIONS, GrantRoleRoutingModule} from  './GrantRole-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    GrantRoleRoutingModule
  ],
  declarations: GRANTROLE_MODULE_DECLARATIONS,
  exports: GRANTROLE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class GrantRoleModule { }