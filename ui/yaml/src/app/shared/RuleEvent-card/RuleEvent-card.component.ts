import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './RuleEvent-card.component.html',
  styleUrls: ['./RuleEvent-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.RuleEvent-card]': 'true'
  }
})

export class RuleEventCardComponent {


}