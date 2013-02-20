# coding: utf-8

from mako.template import Template

template = Template("""# coding: utf-8
Mein Name ist ${name}!
""")

print template.render(name = u"Gerold ÖÄÜ")
