import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {RBACROLE_MODULE_DECLARATIONS, RbacRoleRoutingModule} from  './RbacRole-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    RbacRoleRoutingModule
  ],
  declarations: RBACROLE_MODULE_DECLARATIONS,
  exports: RBACROLE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class RbacRoleModule { }