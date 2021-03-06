#!/bin/sh

# Version: 7.0.0 2020-06-02

# Title: Bootstrap
# Description: Bootstrap test

. pcp-functions

pcp_html_head "Dev bootstrap" "GE"

echo '<hr>'

pcp_activate_tooltip

echo '<div>'
echo '    <ul class="list-inline">'
echo '        <li class="list-inline-item">'
echo '            <a href="#" data-toggle="tooltip" data-placement="top" title="Default tooltip">Tooltip</a>'
echo '        </li>'
echo '        <li class="list-inline-item">'
echo '            <a href="#" data-toggle="tooltip" data-placement="right" title="Another tooltip">Another tooltip</a>'
echo '        </li>'
echo '        <li class="list-inline-item">'
echo '            <a href="#" data-toggle="tooltip" data-placement="bottom" title="A much longer tooltip to demonstrate the max-width of the Bootstrap tooltip.">Large tooltip</a>'
echo '        </li>'
echo '        <li class="list-inline-item">'
echo '            <a href="#" data-toggle="tooltip" data-placement="left" title="The last tip!">Last tooltip</a>'
echo '        </li>'
echo '    </ul>'
echo '</div>'

echo '<button type="button" class="btn btn-secondary" data-toggle="tooltip" data-placement="top" title="Tooltip on top">'
echo '  Tooltip on top'
echo '</button>'
echo '<button type="button" class="btn btn-secondary" data-toggle="tooltip" data-placement="right" title="Tooltip on right">'
echo '  Tooltip on right'
echo '</button>'
echo '<button type="button" class="btn btn-secondary" data-toggle="tooltip" data-placement="bottom" title="Tooltip on bottom">'
echo '  Tooltip on bottom'
echo '</button>'


echo '<!-- HTML to write -->'
echo '<a href="#" data-toggle="tooltip" title="Some tooltip text!">Hover over me!!!!!</a>'
echo ''
echo '<!-- Generated markup by the plugin -->'
echo '<div class="tooltip bs-tooltip-top" role="tooltip">'
echo '  <div class="arrow"></div>'
echo '  <div class="tooltip-inner">'
echo '    Some tooltip text!!!!!'
echo '  </div>'
echo '</div>'


echo '<div class="container">'


echo '<!-- HTML to write -->'

echo '<br>'
echo '<a href="#" data-toggle="tooltip" title="XXXX Some tooltip text!">Hover over me</a>'
echo ''
echo '<!-- Generated markup by the plugin -->'
echo '<div class="tooltip bs-tooltip-top" role="tooltip">'
echo '  <div class="arrow"></div>'
echo '  <div class="tooltip-inner">'
echo '    Some tooltip text!'
echo '  </div>'
echo '</div>'

echo '<hr>'

#echo '  <button id="button" aria-describedby="tooltip">My button</button>'
#echo '  <div id="tooltip" role="tooltip">My tooltip</div>'
#
#echo '  <script>'
#echo '    const button = document.querySelector('#button');'
#echo '    const tooltip = document.querySelector('#tooltip');'
#echo '    Popper.createPopper(button, tooltip);'
#echo '  </script>'


echo '<hr>'

#echo '<a href="#" data-toggle="tooltip" title="Title Here">Hyperlink Text</a>'
#echo ''
#echo '<script>'
#echo '$(document).ready(function() {'
#echo '    $("body").tooltip({ selector: '[data-toggle=tooltip]' });'
#echo '});'
#echo '</script>'

echo '<hr>'

echo '  <div class="container mt-3">'
echo '    <h2>Modal Example</h2>'
echo '    <!-- Button to Open the Modal -->'
echo '    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#myModal">'
echo '      Open modal'
echo '    </button>'
echo '    '
echo '    <!-- The Modal -->'
echo '    <div class="modal fade" id="myModal">'
echo '      <div class="modal-dialog">'
echo '        <div class="modal-content">'
echo '        '
echo '          <!-- Modal Header -->'
echo '          <div class="modal-header">'
echo '            <h5 class="modal-title">Backup configuration</h5>'
echo '            <button type="button" class="close" data-dismiss="modal">×</button>'
echo '          </div>'
echo '          '
echo '          <!-- Modal body -->'
echo '          <div class="modal-body">'
echo '            Modal body..'
echo '          </div>'
echo '          '
echo '          <!-- Modal footer -->'
echo '          <div class="modal-footer">'
echo '            <a type="button" class="btn btn-success" href="backup.cgi">Backup</a>'
echo '            <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button>'
echo '          </div>'
echo '          '
echo '        </div>'
echo '      </div>'
echo '    </div>'
echo '    '
echo '  </div>'

echo '<hr>'

echo '     <div class="clearfix">'
echo '       <button type="button" class="btn btn-secondary float-left">Example left</button>'
echo '       <button type="button" class="btn btn-secondary float-left">Example left</button>'
echo '       <button type="button" class="btn btn-secondary float-right">Example right</button>'
echo '     </div>'

echo '<hr>'

echo '     <div class="row">'
echo '        <div class="col-sm-8">col-sm-8</div>'
echo '        <div class="col-sm-4">col-sm-4</div>'
echo '      </div>'
echo '      <div class="row">'
echo '        <div class="col-sm">col-sm</div>'
echo '        <div class="col-sm">col-sm</div>'
echo '        <div class="col-sm">col-sm</div>'
echo '      </div>'

echo '<hr>'

echo '    <form>'
echo '      <div class="form-group">'
echo '        <label for="exampleFormControlInput1">Email address</label>'
echo '        <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">'
echo '      </div>'
echo '      <div class="form-group">'
echo '        <label for="exampleFormControlSelect1">Example select</label>'
echo '        <select class="form-control" id="exampleFormControlSelect1">'
echo '          <option>1</option>'
echo '          <option>2</option>'
echo '          <option>3</option>'
echo '          <option>4</option>'
echo '          <option>5</option>'
echo '        </select>'
echo '      </div>'
echo '      <div class="form-group">'
echo '        <label for="exampleFormControlSelect2">Example multiple select</label>'
echo '        <select multiple class="form-control" id="exampleFormControlSelect2">'
echo '          <option>1</option>'
echo '          <option>2</option>'
echo '          <option>3</option>'
echo '          <option>4</option>'
echo '          <option>5</option>'
echo '        </select>'
echo '      </div>'
echo '      <div class="form-group">'
echo '        <label for="exampleFormControlTextarea1">Example textarea</label>'
echo '        <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>'
echo '      </div>'
echo '    </form>'

echo '<hr>'

echo '    <div class="custom-control custom-switch">'
echo '      <input type="checkbox" class="custom-control-input" id="customSwitch1">'
echo '      <label class="custom-control-label" for="customSwitch1">Toggle this switch element</label>'
echo '    </div>'
echo '    <div class="custom-control custom-switch">'
echo '      <input type="checkbox" class="custom-control-input" disabled id="customSwitch2">'
echo '      <label class="custom-control-label" for="customSwitch2">Disabled switch element</label>'
echo '    </div>'

echo '<hr>'

echo '    <div class="btn-group" role="group" aria-label="Button group with nested dropdown">'
echo '      <button type="button" class="btn btn-secondary">1</button>'
echo '      <button type="button" class="btn btn-secondary">2</button>'
echo '    '
echo '      <div class="btn-group" role="group">'
echo '        <button id="btnGroupDrop1" type="button" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
echo '          Dropdown'
echo '        </button>'
echo '        <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">'
echo '          <a class="dropdown-item" href="#">Dropdown link</a>'
echo '          <a class="dropdown-item" href="#">Dropdown link</a>'
echo '        </div>'
echo '      </div>'
echo '    </div>'

echo '<hr>'

echo '    <div class="btn-group btn-group-toggle" data-toggle="buttons">'
echo '      <label class="btn btn-secondary active">'
echo '        <input type="radio" name="options" id="option1" checked> Active'
echo '      </label>'
echo '      <label class="btn btn-secondary">'
echo '        <input type="radio" name="options" id="option2"> Radio'
echo '      </label>'
echo '      <label class="btn btn-secondary">'
echo '        <input type="radio" name="options" id="option3"> Television'
echo '      </label>'
echo '    </div>'

echo '<hr>'

echo '    <button type="button" class="btn btn-primary">Primary</button>'
echo '    <button type="button" class="btn btn-secondary">Secondary</button>'
echo '    <button type="button" class="btn btn-success">Success</button>'
echo '    <button type="button" class="btn btn-danger">Danger</button>'
echo '    <button type="button" class="btn btn-warning">Warning</button>'
echo '    <button type="button" class="btn btn-info">Info</button>'
echo '    <button type="button" class="btn btn-light">Light</button>'
echo '    <button type="button" class="btn btn-dark">Dark</button>'
echo ' '
echo '    <button type="button" class="btn btn-link">Link</button>'

echo '<hr>'

echo '    <span class="badge badge-primary">Primary</span>'
echo '    <span class="badge badge-secondary">Secondary</span>'
echo '    <span class="badge badge-success">Success</span>'
echo '    <span class="badge badge-danger">Danger</span>'
echo '    <span class="badge badge-warning">Warning</span>'
echo '    <span class="badge badge-info">Info</span>'
echo '    <span class="badge badge-light">Light</span>'
echo '    <span class="badge badge-dark">Dark</span>'

echo '<hr>'

echo '    <h1>Example heading <span class="badge badge-secondary">New</span></h1>'
echo '    <h2>Example heading <span class="badge badge-secondary">New</span></h2>'
echo '    <h3>Example heading <span class="badge badge-secondary">New</span></h3>'
echo '    <h4>Example heading <span class="badge badge-secondary">New</span></h4>'
echo '    <h5>Example heading <span class="badge badge-secondary">New</span></h5>'
echo '    <h6>Example heading <span class="badge badge-secondary">New</span></h6>'


echo '    <!-- Optional JavaScript -->'
echo '    <!-- jQuery first, then Popper.js, then Bootstrap JS -->'
echo '    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>'
echo '    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>'
echo '    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>'

echo '</div>'

echo '</body>'
echo '</html>'

exit
