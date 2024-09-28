import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {RULECONSTRAINT_MODULE_DECLARATIONS, RuleConstraintRoutingModule} from  './RuleConstraint-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    RuleConstraintRoutingModule
  ],
  declarations: RULECONSTRAINT_MODULE_DECLARATIONS,
  exports: RULECONSTRAINT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class RuleConstraintModule { }