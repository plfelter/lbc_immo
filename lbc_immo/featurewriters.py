import numpy as np
import geojson as gj
from itertools import repeat
import logging


class FeatureWriter:
    attrs = {
        "title": str,
        "url": str,
        "price": int,
        "pictures": lambda x: '\n'.join(['{{' + e + '}}' for e in str(x).split("|||")]),
        "description": str,
        "lat": float,
        "lng": float,
        "last_publication_date": lambda t: t.to_pydatetime(),
        "first_publication_date": lambda t: t.to_pydatetime()
    }

    def __init__(self, e):

        self.feature = None

        if not set(self.attrs).issubset(set(e.index)):
            raise Exception(f"Missing mandatory fields:\n{set(self.attrs) - set(e.index)}")

        try:
            for a, f in self.attrs.items():
                e[a] = f(e[a])
        except ValueError as exc:
            logging.debug(
                f'Dropping entry ; got exception when trying to apply {f} to {e[a]} ({a}): {exc}')
            return

        self._generate_feature(e)

    def _generate_feature(self, e):
        self.feature = gj.Feature(
            geometry=gj.Point((e.lng, e.lat)), 
            properties={
                "name":
                    f"[{int(e.price)}€] {e.title} "
                    f"{e.last_publication_date.strftime('(%d %b %H:%M)')}",
                "description": 
                    '\n'.join(
                        list(map(self.get_attr_str, repeat(e), self.attrs)) + \
                        list(map(self.get_attr_str, repeat(e), set(e.index) - set(self.attrs)))),
                "_umap_options": {
                    "color": "Black" if np.isnan(e.price) else self.get_colour(
                        e.price, 0, 2000),
                    "iconClass": "Circle",
                    "popupShape": "Panel", # "Large"
                    "showLabel": None,
                    "labelDirection": "right",
                    "labelInteractive": False
                }
            }
        )

    def __repr__(self):
        return self.feature.__repr__()

    @staticmethod
    def get_colour(v, vmin, vmax):
        # Return a RGB colour value given a scalar v in the range [vmin,vmax]
        # The colour is clipped at the end of the scales if v is outside the range [vmin,vmax]
        
        # Each colour component ranges from 0 (no contribution) to 1 (fully saturated)
        r, g, b = 1, 0, 1

        v = min(max(v, vmin), vmax)
        dv = vmax - vmin
        r = (v - vmin) / dv
        b = 1 - r

        # Convert to hex string
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

    @staticmethod
    def get_attr_str(e, attr, with_attr_name=True):
        if with_attr_name:
            return f'**{attr}:**\t{e[attr]}'
        else:
            return f'{e[attr]}'


class ImmoFeatureWriter(FeatureWriter):

    attrs = {
        **FeatureWriter.attrs,
        "surface": str
    }

    @staticmethod
    def _extract_eur_per_m2(surf: str, price: int) -> str:
        try:
            return str(int(price / int(surf.split(' ')[0])))
        except Exception:
            return '-'

    @staticmethod
    def _extract_surface(surf: str) -> str:
        try:
            return str(int(surf.split(' ')[0]))
        except Exception:
            return '-'
    
    def _generate_feature(self, e):
        self.feature = gj.Feature(
            geometry=gj.Point((e.lng, e.lat)), 
            properties={
                "name":
                    f"[{int(e.price / 1000)} k€] "
                    f"[{self._extract_surface(e.surface)} m2] "
                    f"[{self._extract_eur_per_m2(e.surface, e.price)} €/m2] "
                    f" {e.title} "
                    f"{e.last_publication_date.strftime('(%d %b %H:%M)')}",
                "description":
                    '\n'.join(list(map(self.get_attr_str, repeat(e), self.attrs))),
                "_umap_options": {
                    "color": "Black" if np.isnan(e.price) else self.get_colour(
                        e.price / 1000, 50, 600),
                    "iconClass": "Circle",
                    "popupShape": "Panel",  # "Large", "Panel",
                    "showLabel": None,
                    "labelDirection": "right",
                    "labelInteractive": False
                }
            }
        )


class ImmoLocFeatureWriter(FeatureWriter):

    attrs = {
        **FeatureWriter.attrs,
        "surface": str,
        "meublé / non meublé": str,
        "nombre de chambres": str,
        "extérieur": str,
        "places de parking": str,
        "étage du bien": str,
        "nombre d'étages de l'immeuble": str,
        "classe énergie": str,
        "pièces": str
    }

    @staticmethod
    def _extract_surface(surf: str) -> str:
        try:
            return str(int(surf.split(' ')[0]))
        except Exception:
            return '-'

    def _generate_feature(self, e):
        self.feature = gj.Feature(
            geometry=gj.Point((e.lng, e.lat)),
            properties={
                "name":
                    f"[{int(e.price)} €/month][{self._extract_surface(e.surface)} m2]"
                    f" {e.title} "
                    f"{e.last_publication_date.strftime('(%d %b %H:%M)')}",
                "description":
                    '\n'.join(list(map(self.get_attr_str, repeat(e), self.attrs))),
                "_umap_options": {
                    "color": "Black" if np.isnan(e.price) else self.get_colour(
                        e.price, 50, 1600),
                    "iconClass": "Circle",
                    "popupShape": "Panel",  # "Large", #"Panel",
                    "showLabel": None,
                    "labelDirection": "right",
                    "labelInteractive": False
                }
            }
        )
