from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Props(models.Model):
    id = models.BigIntegerField(db_column='id', primary_key=True)
    Name = models.TextField(db_column='Name', blank=True, null=True)
    Length = models.FloatField(db_column='Length', blank=True, null=True)
    Mass = models.FloatField(db_column='Mass', blank=True, null=True)
    SASAmiller = models.FloatField(db_column='SASAmiller', blank=True, null=True)
    NetCh = models.FloatField(db_column='NetCh', blank=True, null=True)
    NCD = models.FloatField(db_column='NCD', blank=True, null=True)
    fFatty = models.FloatField(db_column='fFatty', blank=True, null=True)
    fPos = models.FloatField(db_column='fPos', blank=True, null=True)
    fNeg = models.FloatField(db_column='fNeg', blank=True, null=True)
    GC = models.FloatField(db_column='GC', blank=True, null=True)
    seqnum = models.FloatField(db_column='SeqNum', blank=True, null=True)
    fCharged = models.FloatField(db_column='fCharged', blank=True, null=True)
    ncd1000 = models.FloatField(db_column='NCD1000', blank=True, null=True)
    mwkda = models.FloatField(db_column='MWkDa', blank=True, null=True)
    i = models.FloatField(db_column='I', blank=True, null=True)
    l = models.FloatField(db_column='L', blank=True, null=True)
    v = models.FloatField(db_column='V', blank=True, null=True)
    a = models.FloatField(db_column='A', blank=True, null=True)
    g = models.FloatField(db_column='G', blank=True, null=True)
    p = models.FloatField(db_column='P', blank=True, null=True)
    f = models.FloatField(db_column='F', blank=True, null=True)
    m = models.FloatField(db_column='M', blank=True, null=True)
    w = models.FloatField(db_column='W', blank=True, null=True)
    y = models.FloatField(db_column='Y', blank=True, null=True)
    h = models.FloatField(db_column='H', blank=True, null=True)
    t = models.FloatField(db_column='T', blank=True, null=True)
    s = models.FloatField(db_column='S', blank=True, null=True)
    n = models.FloatField(db_column='N', blank=True, null=True)
    q = models.FloatField(db_column='Q', blank=True, null=True)
    d = models.FloatField(db_column='D', blank=True, null=True)
    e = models.FloatField(db_column='E', blank=True, null=True)
    k = models.FloatField(db_column='K', blank=True, null=True)
    r = models.FloatField(db_column='R', blank=True, null=True)
    c = models.FloatField(db_column='C', blank=True, null=True)
    x = models.FloatField(db_column='X', blank=True, null=True)
    u = models.FloatField(db_column='U', blank=True, null=True)
    kingdom = models.TextField(blank=True, null=True)
    phylum = models.TextField(blank=True, null=True)
    taxClass = models.TextField(db_column='class', blank=True, null=True)
    order = models.TextField(blank=True, null=True)
    family = models.TextField(blank=True, null=True)
    genus = models.TextField(blank=True, null=True)
    species = models.TextField(db_column='species', blank=True, null=True)
    taxid = models.TextField(db_column='Taxid', blank=True, null=True)
    dataset = models.TextField(db_column="dataset", null=False)


    class Meta:
        managed = True
        db_table = 'Props'

    def __str__(self):
        return f"{self.Name}; {self.species} ({self.kingdom})"

    def serialize(self):
        """Dictionary representation of properties"""
        result = dict()
        for field_name in [field.name for field in self._meta.fields]:
            result.update( {field_name : self.__dict__[field_name]} )

        return result

    def lineage(self):
        result = ""
        for field_name in ["kingdom", "phylum", "taxClass", "order", "family", "species"]:
            result += " {};".format(self.__dict__[field_name])

        return result
