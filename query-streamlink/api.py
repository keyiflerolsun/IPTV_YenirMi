import streamlink
from streamlink import NoPluginError, PluginError


def get_streams(query):
    """
    Get data streams
    Returns: (links), Error string
    """
    try:
        streams = list(streamlink.streams(query).items())
        if not streams:
            return "No streams found."
        for quality, link in streams:
                # Suggest that if there's no multiple qualities (live),
                # give manifest (master) URL.
            return link.to_url() if ("live" not in quality or "best" in quality) and "chunklist" in link.to_url() or "live" in quality and "best" not in quality else link.to_manifest_url()

    except ValueError as ex:
        return f"Streamlink couldn't read {query}, for this reason : {ex}"
    except NoPluginError:
        return f"Streamlink was unable to process your query, because no plugin has been implemented for website {query}"
    except PluginError as pex:
        return f"Streamlink couldn't process {query}, because of a Plugin error. Reason is as follows: {pex}"