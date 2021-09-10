from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from .models import Attendee
import datetime

def k_means_event(user):
    print("girdi")
    scaler = StandardScaler()
    array = []
    labels = []
    attendee = Attendee.objects.filter(user=user)
    if(not attendee):
        return [], [], []
    n_clusters = user.attended_events.count()//4 + 1
    print("n_clusters:")
    print(n_clusters)
    for item in attendee:
        event= item.event
        labels.append(event.pk)
        print(event.pk)
        array_item = [event.category.id, event.date.hour, event.date.weekday()]
        array.append(array_item)
    scaled_events = scaler.fit_transform(array)
    print(scaled_events)
    kmeans = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10, max_iter=200)
    event_clusters = kmeans.fit(scaled_events).labels_
    cluster_labels = [[] for i in range(n_clusters)]
    for i, j in enumerate(event_clusters):
        cluster_labels[j].append(labels[i])
    print("event_clusters")
    print(event_clusters)
    print("cluster_labels")
    print(cluster_labels)
    print("kmeans")
    print(kmeans)
    print(kmeans.cluster_centers_)
    return event_clusters, kmeans, cluster_labels
    