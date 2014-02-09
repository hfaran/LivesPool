def banner_title(title):
    """banner_title"""
    s = """
        <div class="row">
            <div class="col-xs-12">
                <h1>
                    {title}
                </h1>
            </div>
        </div>
    """
    return s.format(title=title)

def load_bootstrap():
    """load_bootstrap"""
    s = """
        <link rel="stylesheet" media="screen" href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.0/css/bootstrap.min.css">
        <link rel="stylesheet" media="screen" href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.0/css/bootstrap-theme.min.css">
    """
    return s

def global_meta_tags():
    s = """
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """
    return s
