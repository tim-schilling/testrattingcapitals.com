<!DOCTYPE html>
<html>
<head>
<title>TEST Ratting Capitals</title>
<style>
    body {
        margin: 0 auto;
        font-family: Helvetica, Arial, sans-serif;
        text-align: center;
        font-size: 24pt;
    }

    a {
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }

    .container strong {
			color: #900;
			font-size: 36pt;
			font-weight: bold;
    }

    .container p.callout {
      font-size: 12pt;
    }

    .container p.shame {
      font-size: 8pt;
      text-decoration: none;
      position: absolute;
      bottom: 0;
      text-align: center;
      margin: 1em auto;
      width: 100%;
    }
</style>
</head>
<body>
<div class="container">
</div>

<script type="text/javascript" src="//code.jquery.com/jquery-1.12.4.min.js"></script>
<script type="text/javascript">
  $(function() {
    $.getJSON('/data.json',
      function(data) {
        if (!data || typeof(data) !== 'object' || data.hasOwnProperty('daysSince') === false) {
          return $('.container').html('<p>RIP. An error has occurred.</p>');
        }

        if (data.daysSince < 0) {
          return $('.container').html('<p>You\'ve created a time paradox.</p>');
        }

        var BODY_FORMAT = [
          '<p>It has been <strong>{{DAYS_SINCE}}</strong> days since a TEST ratting capital died.</p>',
          '<p class="callout"><a href="{{ZKILL_URL}}">{{ZKILL_URL}}</a></p>',
          '<p class="shame"><a href="https://zkillboard.com/alliance/498125261/losses/group/547,513,902,941,30,659,883/">Wall of shame</a></p>'
        ]
        .join('\n')

        var result = BODY_FORMAT
        .replace(new RegExp('{{DAYS_SINCE}}', 'g'), data.daysSince)
        .replace(new RegExp('{{ZKILL_URL}}', 'g'), data.url);

        $('.container').html(result);
      }
    );
  });
</script>
</body>
</html>
