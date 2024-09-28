import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './RuleDerivation-card.component.html',
  styleUrls: ['./RuleDerivation-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.RuleDerivation-card]': 'true'
  }
})

export class RuleDerivationCardComponent {


}