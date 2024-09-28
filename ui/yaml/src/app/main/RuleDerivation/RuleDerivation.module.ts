import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {RULEDERIVATION_MODULE_DECLARATIONS, RuleDerivationRoutingModule} from  './RuleDerivation-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    RuleDerivationRoutingModule
  ],
  declarations: RULEDERIVATION_MODULE_DECLARATIONS,
  exports: RULEDERIVATION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class RuleDerivationModule { }